# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Store_Issue_ProductForm,Store_issue_Form
from ..models import Store_Issue_Note, Store_Issue_Product ,Product,Inventory,Final_Product
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum
from django.http import JsonResponse
from collections import defaultdict
from django.db import IntegrityError


@login_required
@permission_required('home.view_store_issue_note', login_url='/login/')
def list_store_issue(request):
    store_issue_items_pro = {}
    issuereceipts = Store_Issue_Note.objects.all()
    for x in issuereceipts:
        # Count the number of products for each sale receipt
        store_issue_items_pro[x.id] = Store_Issue_Product.objects.filter(store_issue_note=x).count()
    return render(request, 'store_issue/list_store_issue.html', {
        'issuereceipts': issuereceipts,
        'issuereceipts_items_pro': store_issue_items_pro,
    
    })


@login_required
@permission_required('home.add_store_issue_note', login_url='/login/')
def create_store_issue_note(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:  # Finalize the purchase note
            form_store_issue = Store_issue_Form(request.POST)
            products = request.POST.getlist('products[]')
            if form_store_issue.is_valid() and products:
                store_issue = form_store_issue.save(commit=False)
                store_issue.created_by = request.user
                store_issue.save()

                # for product_data in products:
                #     print(product_data)
                #     product_id, quantity = product_data.split(':')
                #     Store_Issue_Product.objects.create(
                #         store_issue_note=store_issue,
                #         product_id=product_id,
                #         quantity=quantity
                #     )

                for product_data in products:
                    product_id, quantity = product_data.split(':')
                    Store_Issue_Product.objects.create(
                        store_issue_note=store_issue,
                        product_id=product_id,
                        quantity=quantity
                    )
                    Product.objects.get(id=product_id).change_status()

                return JsonResponse({'success': True, 'redirect_url': '/list-store-issue/'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = Store_Issue_ProductForm()
        form_store_issue = Store_issue_Form()
    return render(request, 'store_issue/create_issue_note.html', {
        'form': form,
        'form_store_issue': form_store_issue,
    })


@login_required
@permission_required('home.change_store_issue_note', login_url='/login/')

def edit_store_issue_note(request, issue_note_id):
    print("i m called")
    grn = get_object_or_404(Store_Issue_Note, id=issue_note_id)
    products = Store_Issue_Product.objects.filter(store_issue_note=grn.id)
    if request.method == 'POST':
        form = Store_issue_Form(request.POST, instance=grn)
        if form.is_valid():
            grn = form.save()
            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')
            # Delete removed products
            Store_Issue_Product.objects.filter(store_issue_note=grn, product__id__in=deleted_products).delete()
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
                    product, created = Store_Issue_Product.objects.update_or_create(
                        store_issue_note=grn, 
                        product=product_instance, 
                        defaults={'quantity': total_quantity}
                    )
                    Product.objects.get(id=product_id).change_status()
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with ID {product_id} does not exist.'})

            return JsonResponse({'success': True, 'redirect_url': '/list-store-issue/'})

        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    context = {
        'grn': grn,
        'products': products,
        'form': Store_issue_Form(instance=grn),
        'product_form': Store_Issue_ProductForm(),
    }
    return render(request, 'store_issue/edit_issue_note.html', context)

@login_required
@permission_required('home.view_store_issue_note', login_url='/login/')
def print_store_issue(request, issue_note_id):
    # Fetch the store issue instance by ID
    issue_note = get_object_or_404(Store_Issue_Note, id=issue_note_id)
    # Fetch all products associated with this store issue
    issue_note_products = Store_Issue_Product.objects.filter(store_issue_note=issue_note)
    return render(request, 'store_issue/print_store_issue.html', {
        'issue_note': issue_note,
        'issue_note_products': issue_note_products, 
    })

@login_required
# @permission_required('home.add_store_issue_note' , login_url='/login/')
def get_stock(request,id):
    product=Product.objects.get(id=id)
    stock_qty=product.get_current_stock()
    print(stock_qty)
    print(id,stock_qty)
    return JsonResponse({'success': True,'stock':stock_qty})


@login_required
@permission_required('home.delete_store_issue_note', login_url='/login/')
def delete_store_issue(request, id):
    product_list=[]
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        store_issue = get_object_or_404(Store_Issue_Note, id=id)
        store_issue_products = Store_Issue_Product.objects.filter(store_issue_note=store_issue)
        if store_issue_products:
            for pro in store_issue_products:
                product_list.append(pro.product)
            store_issue_products.delete()  # Bulk delete all related products
            for pro in product_list:
                pro.change_status()
        store_issue.delete()
        return JsonResponse({'success': True, 'message': 'Store issue note deleted successfully!'})
    
    # For non-AJAX requests, handle as usual
    store_issue = get_object_or_404(Store_Issue_Note, id=id)
    store_issue_products = Store_Issue_Product.objects.filter(store_isuue_note=store_issue)
    if store_issue_products:
        for pro in store_issue_products:
            product_list.append(pro.product)
        store_issue_products.delete()  # Bulk delete all related products
        for pro in product_list:
            pro.change_status()
    store_issue.delete()
    messages.success(request, "Store issue note deleted successfully!")
    return redirect('list_store_issue')

