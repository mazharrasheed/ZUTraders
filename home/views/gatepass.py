# # Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  GatePassProductForm,GatePassForm
from ..models import GatePass, GatePassProduct,Product
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.contrib import messages
from collections import defaultdict

from ..forms import GatePassForm, GatePassProductForm
from ..models import GatePass, GatePassProduct, Product


@login_required
@permission_required('home.view_gatepass', login_url='/login/')
def list_gatepasses(request):
    gatepass_items_pro={}
    gatepasses = GatePass.objects.all()
    gatepasses
    gatepass_products = GatePassProduct.objects.all().count()
    for x in gatepasses:
        gatepass_items_pro[x.id] = GatePassProduct.objects.filter(gatepass=x).count()

    return render(request, 'gatepass/list_gatepasses.html', {
        'gatepasses': gatepasses,
        'gatepass_items_pro': gatepass_items_pro,
        })


@login_required
@permission_required('home.add_gatepass', login_url='/login/')
def create_gatepass(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:
            form_gate_pass = GatePassForm(request.POST)
            products = request.POST.getlist('products[]')
            if form_gate_pass.is_valid() and products:
                gate_pass = form_gate_pass.save(commit=False)
                gate_pass.save()
                for product_data in products:
                    product_id, quantity, remarks = product_data.split(':')
                    GatePassProduct.objects.create(
                        gatepass=gate_pass,
                        product_id=product_id,
                        quantity=quantity,
                        remarks=remarks
                    )
                    Product.objects.get(id=product_id).change_status()
                return JsonResponse({'success': True, 'redirect_url': '/list-gatepasses/'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = GatePassProductForm()
        form_gate_pass = GatePassForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gate_pass': form_gate_pass,
    })

@login_required
@permission_required('home.change_gatepass', login_url='/login/')
def edit_gatepass(request, gatepass_id):
    gate_pass = get_object_or_404(GatePass, id=gatepass_id)
    products = GatePassProduct.objects.filter(gatepass=gate_pass)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = GatePassForm(request.POST, instance=gate_pass)

        if form.is_valid():
            gate_pass = form.save()

            # Handle products
            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')

            print(deleted_products, 'Received deleted product IDs')

            # Delete removed products
            if deleted_products:
                try:
                    deleted_product_ids = [int(pid) for pid in deleted_products]
                    GatePassProduct.objects.filter(
                        gatepass=gate_pass,
                        product__id__in=deleted_product_ids
                    ).delete()
                    print(f"Deleted products with IDs: {deleted_product_ids}")
                except ValueError as e:
                    print(f"Error converting product IDs to int: {e}")

            # Add/Update products
            for product_info in product_data:
                try:
                    product_id, quantity, remarks = product_info.split(':')
                    GatePassProduct.objects.update_or_create(
                        gatepass=gate_pass,
                        product_id=product_id,
                        defaults={'quantity': quantity, 'remarks': remarks}
                    )
                    Product.objects.get(id=product_id).change_status()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Invalid product data.'})

            return JsonResponse({'success': True, 'redirect_url': '/list-gatepasses/'})
        else:
            # Return validation errors for gatepass form
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    context = {
        'gate_pass': gate_pass,
        'products': products,
        'form': GatePassForm(instance=gate_pass),
        'product_form': GatePassProductForm(),
    }
    return render(request, 'gatepass/edit_gatepass.html', context)



@login_required
@permission_required('home.delete_gatepass', login_url='/login/')
def delete_gatepass(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        gate_pass = get_object_or_404(GatePass, id=id)
        gate_pass_products = GatePassProduct.objects.filter(gatepass=gate_pass)
        for gp in gate_pass_products:
            gp.product.change_status()
        gate_pass_products.delete()
        gate_pass.delete()
        return JsonResponse({'success': True, 'message': 'Gate pass deleted successfully!'})
    else:
        return redirect('list_gatepasses')

@login_required
def get_stock(request, id):
    product = get_object_or_404(Product, id=id)
    stock_qty = product.get_current_stock()
    return JsonResponse({'success': True, 'stock': stock_qty})


@login_required
@permission_required('home.delete_gatepass', login_url='/login/')
def delete_gatepass_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(GatePassProduct, id=id)
        gatepass_id = request.POST.get('gatepass_id')
        product.delete()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def cancel_gatepass(request,id):
    # gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    # 
    if gatepass_products:
        for item in gatepass_products:
            item.delete()
    gatepass.delete()
    messages.success(request, "Your gatepass canceled !") 
    return redirect('list_gatepasses')

@login_required
def delete_gatepass1(request,id):
    print('i m delete item')
    # gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    if gatepass_products:
        for item in gatepass_products:
            item.delete()
    gatepass.delete()
    messages.success(request, "Gatepass deleted successful!")    
    return redirect('list_gatepasses')

# def delete_gatepass(request, id):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
#         gatepass = get_object_or_404(GatePass, id=id)
#         gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
#         if gatepass_products:
#             gatepass_products.delete()  # Bulk delete all related products
#         gatepass.delete()
#         return JsonResponse({'success': True, 'message': 'Gatepass deleted successfully!'})
    
#     # For non-AJAX requests, handle as usual
#     gatepass = get_object_or_404(GatePass, id=id)
#     gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
#     if gatepass_products:
#         gatepass_products.delete()  # Bulk delete all related products
#     gatepass.delete()
#     messages.success(request, "Gatepass deleted successfully!")
#     return redirect('list_gatepasses')



@login_required
def print_gatepass(request, gatepass_id):
    # Fetch the GatePass instance by ID
    gatepass = get_object_or_404(GatePass, id=gatepass_id)
    # Fetch all products associated with this GatePass
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)

    return render(request, 'gatepass/print_gatepass.html', {
        'gatepass': gatepass,
        'gatepass_products': gatepass_products,
        
    })

