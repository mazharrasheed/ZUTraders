# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Store_Purchase_ProductForm,Store_Purchase_Form
from ..models import Store_Purchase_Note, Store_Purchase_Product ,Product
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum

@login_required
@permission_required('home.view_store_purchase_note', login_url='/login/')
def list_store_purchase(request):
    purchasereceipts_items_pro = {}
    salereceipts=[]
    purchasereceipts = Store_Purchase_Note.objects.all()
    
    for x in purchasereceipts:
        # Count the number of products for each sale receipt
        purchasereceipts_items_pro[x.id] = Store_Purchase_Product.objects.filter(store_purchase_note=x).count()

    return render(request, 'store_purchase/list_store_purchase.html', {
        'purchasereceipts': purchasereceipts,
        'purchasereceipts_items_pro': purchasereceipts_items_pro,
    
    })


@login_required
@permission_required('home.add_store_purchase_note', login_url='/login/')
def create_store_purchase(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:  # Finalize the purchase note
            form_salereceipt = Store_Purchase_Form(request.POST)
            products = request.POST.getlist('products[]')
            
            if form_salereceipt.is_valid() and products:
                salereceipt = form_salereceipt.save(commit=False)
                salereceipt.created_by = request.user
                salereceipt.save()

                for product_data in products:
                    product_id, quantity = product_data.split(':')
                    Store_Purchase_Product.objects.create(
                        store_purchase_note=salereceipt,
                        product_id=product_id,
                        quantity=quantity
                    )

                    Product.objects.get(id=product_id).change_status()

                return JsonResponse({'success': True, 'redirect_url': '/list-store-purchase/'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = Store_Purchase_ProductForm()
        form_salereceipt = Store_Purchase_Form()

    return render(request, 'store_purchase/create_purchase_note.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
    })




@login_required
@permission_required('home.add_store_purchase_note', login_url='/login/')
def create_store_purchaseold(request, salereceipt_id=None):
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Purchase_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Purchase_Note.objects.create()
        return redirect('create_store_purchase', salereceipt_id=salereceipt.id)
    if request.method == 'POST':
        form = Store_Purchase_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_Purchase_Form(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            project=form_salereceipt.cleaned_data.get('project_name')
            product=form.cleaned_data.get('product')
            salereceipt_product = form.save(commit=False)
            salereceipt_product.store_purchase_note = salereceipt
            salereceipt_product.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
                rendered_products = render_to_string('store_purchase/purchase_note_product_list.html', {
                    'salereceipt_products': salereceipt_products,
                    'salereceipt_id': salereceipt.id,
                })
                return JsonResponse({
                    'success': True,
                    'rendered_products': rendered_products,
                    'salereceipt_id': salereceipt.id,
                })
            return redirect('create_salereceipt', salereceipt_id=salereceipt.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Store_Purchase_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_Purchase_Form(instance=salereceipt)

    salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
    return render(request, 'store_purchase/create_purchase_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })


from collections import defaultdict
from django.db import IntegrityError

def edit_store_purchase(request, salereceipt_id):
    grn = get_object_or_404(Store_Purchase_Note, id=salereceipt_id)
    products = Store_Purchase_Product.objects.filter(store_purchase_note=grn.id)
    
    if request.method == 'POST':
        form = Store_Purchase_Form(request.POST, instance=grn)
        
        if form.is_valid():
            grn = form.save()

            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')

            # Delete removed products
            Store_Purchase_Product.objects.filter(store_purchase_note=grn, product__id__in=deleted_products).delete()
            
            product_quantities = defaultdict(int)
            for product_info in product_data:
                try:
                    product_id, quantity = product_info.split(':')
                    product_quantities[product_id] += int(quantity)
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Invalid product data.'})

            for product_id, total_quantity in product_quantities.items():
                try:
                    product_instance = Product.objects.get(id=product_id)
                    product, created = Store_Purchase_Product.objects.update_or_create(
                        store_purchase_note=grn, 
                        product=product_instance, 
                        defaults={'quantity': total_quantity}
                    )
                    Product.objects.get(id=product_id).change_status()
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with ID {product_id} does not exist.'})

            return JsonResponse({'success': True, 'redirect_url': '/list-store-purchase/'})

        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    context = {
        'grn': grn,
        'products': products,
        'form': Store_Purchase_Form(instance=grn),
        'product_form': Store_Purchase_ProductForm(),
    }
    return render(request, 'store_Purchase/edit_Purchase_note.html', context)

@login_required
@permission_required('home.change_store_purchase_note', login_url='/login/')
def edit_store_purchase_old(request, salereceipt_id=None):
    update=True
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Purchase_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Purchase_Note.objects.create()
        return redirect('create_store_purchase', salereceipt_id=salereceipt.id)
    if request.method == 'POST':
        form = Store_Purchase_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_Purchase_Form(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            project=form_salereceipt.cleaned_data.get('project_name')
            product=form.cleaned_data.get('product')
       
            salereceipt_product = form.save(commit=False)
            salereceipt_product.store_purchase_note = salereceipt
            salereceipt_product.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
                rendered_products = render_to_string('store_purchase/purchase_note_product_list.html', {
                    'salereceipt_products': salereceipt_products,
                    'salereceipt_id': salereceipt.id,
                })
                return JsonResponse({
                    'success': True,
                    'rendered_products': rendered_products,
                    'salereceipt_id': salereceipt.id,
                })
            return redirect('create_salereceipt', salereceipt_id=salereceipt.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Store_Purchase_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_Purchase_Form(instance=salereceipt)

    salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
    return render(request, 'store_Purchase/edit_Purchase_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
        'update':update
    })



@login_required
@permission_required('home.add_store_Purchase_note', login_url='/login/')
def cancel_store_purchase(request,id):
    # salereceipt_id=(request.GET.get('salereceipt_id'))
    salereceipt=get_object_or_404(Store_Purchase_Note,id=id)
    salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
    # 
    if salereceipt_products:
        for item in salereceipt_products:
            item.delete()
    salereceipt.delete()
    messages.success(request, "Your goods received note canceled !") 
    return redirect('list_store_purchase')


@login_required
@permission_required('home.delete_store_purchase_note', login_url='/login/')
def delete_store_purchase_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(Store_Purchase_Product, id=id)
        salereceipt_id = request.POST.get('salereceipt_id')
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@permission_required('home.view_store_purchase_note', login_url='/login/')
def print_store_purchase(request, salereceipt_id):
    # Fetch the salereceipt instance by ID
    salereceipt = get_object_or_404(Store_Purchase_Note, id=salereceipt_id)
    # Fetch all products associated with this salereceipt
    salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
    return render(request, 'store_purchase/print_store_purchase.html', {
        'salereceipt': salereceipt,
        'salereceipt_products': salereceipt_products, 
    })

@login_required
@permission_required('home.delete_store_purchase_note', login_url='/login/')
def delete_store_purchase(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        salereceipt = get_object_or_404(Store_Purchase_Note, id=id)
        salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
        if salereceipt_products:
            salereceipt_products.delete()  # Bulk delete all related products
        salereceipt.delete()
        return JsonResponse({'success': True, 'message': 'Store purchase note deleted successfully!'})
    
    # For non-AJAX requests, handle as usual
    salereceipt = get_object_or_404(Store_Purchase_Note, id=id)
    salereceipt_products = Store_Purchase_Product.objects.filter(store_purchase_note=salereceipt)
    if salereceipt_products:
        salereceipt_products.delete()  # Bulk delete all related products
    salereceipt.delete()
    messages.success(request, "Sale receipt deleted successfully!")
    return redirect('list_salereceipts')