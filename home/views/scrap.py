
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  GatePassProductForm,GatePassForm
from ..models import GatePass, GatePassProduct,Product
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Store_Issue_ProductForm,Store_issue_Form
from ..models import Store_Issue_Note, Store_Issue_Product ,Product,Inventory
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum
from django.http import JsonResponse


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def create_store_issue(request, salereceipt_id=None):
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Issue_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Issue_Note.objects.create()
        return redirect('create_store_issue', salereceipt_id=salereceipt.id)
    
    if request.method == 'POST':
        form = Store_Issue_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(request.POST, instance=salereceipt)
        
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt = form_salereceipt.save(commit=False)
            salercpt.created_by = request.user
            salercpt.save()
            
            product = form.cleaned_data.get('product')
            quantity_requested = form.cleaned_data.get('quantity')
            print(product.productname,"ghg")
            
            # Check product inventory quantity
            try:
                inventory = Inventory.objects.get(product=product)
                if inventory.quantity < quantity_requested:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': f'Insufficient stock for {product.productname}. Available: {inventory.quantity}, Requested: {quantity_requested}'
                        })
                    else:
                        form.add_error('quantity', f'Insufficient stock for {product.productname}. Available: {inventory.quantity}, Requested: {quantity_requested}')
                else:
                    # If sufficient inventory, proceed to save the sale receipt product
                    salereceipt_product = form.save(commit=False)
                    salereceipt_product.store_isuue_note = salereceipt
                    salereceipt_product.save()

                    # Update the inventory (reduce quantity)
                    inventory.quantity -= quantity_requested
                    inventory.save()
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
                        rendered_products = render_to_string('store_issue/issue_note_product_list.html', {
                            'salereceipt_products': salereceipt_products,
                            'salereceipt_id': salereceipt.id,
                        })
                        return JsonResponse({
                            'success': True,
                            'rendered_products': rendered_products,
                            'salereceipt_id': salereceipt.id,
                        })
                    return redirect('create_store_issue', salereceipt_id=salereceipt.id)
            
            except Inventory.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': f'No inventory found for {product.name}.'
                    })
                else:
                    form.add_error('product', f'No inventory found for {product.name}.')
        
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Store_Issue_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(instance=salereceipt)

    salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
    return render(request, 'store_issue/create_issue_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })
@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def edit_store_issue(request, salereceipt_id=None):
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Issue_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Issue_Note.objects.create()
        return redirect('create_store_issue', salereceipt_id=salereceipt.id)
    
    if request.method == 'POST':
        form = Store_Issue_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(request.POST, instance=salereceipt)
        
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt = form_salereceipt.save(commit=False)
            salercpt.created_by = request.user
            salercpt.save()
            
            product = form.cleaned_data.get('product')
            quantity_requested = form.cleaned_data.get('quantity')
            print(product.productname,"ghg")
            
            # Check product inventory quantity
            try:
                inventory = Inventory.objects.get(product=product)
                if inventory.quantity < quantity_requested:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': f'Insufficient stock for {product.productname}. Available: {inventory.quantity}, Requested: {quantity_requested}'
                        })
                    else:
                        form.add_error('quantity', f'Insufficient stock for {product.productname}. Available: {inventory.quantity}, Requested: {quantity_requested}')
                else:
                    # If sufficient inventory, proceed to save the sale receipt product
                    salereceipt_product = form.save(commit=False)
                    salereceipt_product.store_isuue_note = salereceipt
                    salereceipt_product.save()

                    # Update the inventory (reduce quantity)
                    inventory.quantity -= quantity_requested
                    inventory.save()
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
                        rendered_products = render_to_string('store_issue/issue_note_product_list.html', {
                            'salereceipt_products': salereceipt_products,
                            'salereceipt_id': salereceipt.id,
                        })
                        return JsonResponse({
                            'success': True,
                            'rendered_products': rendered_products,
                            'salereceipt_id': salereceipt.id,
                        })
                    return redirect('create_store_issue', salereceipt_id=salereceipt.id)
            
            except Inventory.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': f'No inventory found for {product.name}.'
                    })
                else:
                    form.add_error('product', f'No inventory found for {product.name}.')
        
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Store_Issue_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(instance=salereceipt)

    salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
    return render(request, 'store_issue/edit_issue_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })




@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def create_store_issue1(request, salereceipt_id=None):
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Issue_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Issue_Note.objects.create()
        return redirect('create_store_issue', salereceipt_id=salereceipt.id)
    if request.method == 'POST':
        form = Store_Issue_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            project=form_salereceipt.cleaned_data.get('project_name')
           
            product = form.cleaned_data.get('product')
            quantity_requested = form.cleaned_data.get('quantity')

            print(project,product)
            salereceipt_product = form.save(commit=False)
            salereceipt_product.store_isuue_note = salereceipt
            salereceipt_product.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
                rendered_products = render_to_string('store_issue/issue_note_product_list.html', {
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
        form = Store_Issue_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(instance=salereceipt)

    salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
    return render(request, 'store_issue/create_issue_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })

@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def edit_store_issue1(request, salereceipt_id=None):
    update=True
    if salereceipt_id:
        salereceipt = get_object_or_404(Store_Issue_Note, id=salereceipt_id)
    else:
        salereceipt = Store_Issue_Note.objects.create()
        return redirect('create_store_issue', salereceipt_id=salereceipt.id)
    if request.method == 'POST':
        form = Store_Issue_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            project=form_salereceipt.cleaned_data.get('project_name')
            product=form.cleaned_data.get('product')
            print(project,product)
            salereceipt_product = form.save(commit=False)
            salereceipt_product.store_isuue_note = salereceipt
            salereceipt_product.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
                rendered_products = render_to_string('store_issue/issue_note_product_list.html', {
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
        form = Store_Issue_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Store_issue_Form(instance=salereceipt)

    salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
    return render(request, 'store_issue/edit_issue_note.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
        'update':update
    })



@login_required
@permission_required('home.add_store_issue_note', login_url='/login/')
def cancel_store_issue(request,id):
    # salereceipt_id=(request.GET.get('salereceipt_id'))
    salereceipt=get_object_or_404(Store_Issue_Note,id=id)
    salereceipt_products = Store_Issue_Product.objects.filter(store_isuue_note=salereceipt)
    # 
    if salereceipt_products:
        for item in salereceipt_products:
            item.delete()
    salereceipt.delete()
    messages.success(request, "Your store issue note canceled !") 
    return redirect('list_store_issue')


@login_required
@permission_required('home.delete_store_issue_note', login_url='/login/')
def delete_store_issue_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(Store_Issue_Product, id=id)
        salereceipt_id = request.POST.get('salereceipt_id')
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})











product_list=[]

@login_required
def gatepass(request):

    if 'gatepass_products' in request.session:
        del request.session['gatepass_products']

    form = GatePassProductForm()
    form_gatepass=GatePassForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass':form_gatepass,   
    })

# @login_required
# def create_gatepass(request, gatepass_id=None):
#     if gatepass_id:
#         gatepass = get_object_or_404(GatePass, id=gatepass_id)
#     else:
#         gatepass = GatePass.objects.create()
#         print('i m here 222')
#         if request.method == 'POST':
#             form = GatePassProductForm(request.POST)
#             form_gatepass = GatePassForm(request.POST, instance=gatepass)
#             if form.is_valid() and form_gatepass.is_valid():
#                 # Update the GatePass object with the form_gatepass data
#                 form_gatepass.save()  # This will update the existing instance
                
#                 # Save the GatePassProduct object and associate it with the updated GatePass
#                 gatepass_product = form.save(commit=False)
#                 gatepass_product.gatepass = gatepass
#                 gatepass_product.save()
#                 return redirect('create_gatepass', gatepass_id=gatepass.id)

#     if request.method == 'POST':
#         print('i m here')
#         form = GatePassProductForm(request.POST)
#         form_gatepass = GatePassForm(request.POST, instance=gatepass)
#         if form.is_valid() and form_gatepass.is_valid():
#             # Update the GatePass object with the form_gatepass data
#             form_gatepass.save()  # This will update the existing instance
            
#             # Save the GatePassProduct object and associate it with the updated GatePass
#             gatepass_product = form.save(commit=False)
#             gatepass_product.gatepass = gatepass
#             gatepass_product.save()
#             return redirect('create_gatepass', gatepass_id=gatepass.id)
#     else:
#         form = GatePassProductForm()
#         form_gatepass=GatePassForm(instance=gatepass)
#     gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
#     return render(request, 'gatepass/create_gatepass.html', {
#         'form': form,
#         'gatepass_products': gatepass_products,
#         'form_gatepass':form_gatepass,
#         'gatepass': gatepass,
#     })
'''
@login_required
def create_gatepass(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = None
    if request.method == 'POST':
        form_gatepass = GatePassForm(request.POST, instance=gatepass)
        form = GatePassProductForm(request.POST)

        if 'add_product' in request.POST:
            if form.is_valid():
                gatepass_products = request.session.get('gatepass_products', [])
                product_id = form.cleaned_data['product'].id
                quantity = form.cleaned_data['quantity']
                remarks = form.cleaned_data['remarks']
                pro=get_object_or_404(Product, id=product_id)
                unit=pro.unit.name
                weight=int(pro.product_weight)*int(quantity)
                
                print(gatepass_products,type(gatepass_products))

                for i in gatepass_products:
                    print(i['product_id'])
                    if i['product_id']==form.cleaned_data['product'].id:
                        print("product already added")
                        
                    else:
                        print("product added successfuly")
                        break
                        
                gatepass_products.append({
                            'product_id': product_id,
                            'product_name': form.cleaned_data['product'].productname,
                            'quantity': quantity,
                            'unit':unit,
                            "weight":weight,
                            'remarks': remarks,
                            
                        })

                request.session['gatepass_products'] = gatepass_products
                form = GatePassProductForm()

        elif 'finalize_gatepass' in request.POST:
            if form_gatepass.is_valid():
                if not gatepass:
                    gatepass = form_gatepass.save()
                else:
                    form_gatepass.save()

                gatepass_products = request.session.pop('gatepass_products', [])
                for gp in gatepass_products:
                    product = get_object_or_404(Product, id=gp['product_id'])
                  
                    GatePassProduct.objects.create(
                        gatepass=gatepass,
                        product=product,
                        quantity=gp['quantity'],
                        remarks=gp['remarks']
                    )
                return redirect('list_gatepasses')

    else:
        form = GatePassProductForm()
        form_gatepass = GatePassForm(instance=gatepass)

    gatepass_products = request.session.get('gatepass_products', [])

    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass': form_gatepass,
        'gatepass_products': gatepass_products,
        'gatepass': gatepass,
    })
    
'''

def create_gatepass(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = None

    # Initialize form_gatepass with GET or POST data
    form_gatepass = GatePassForm(request.POST or None, instance=gatepass)
    
    if request.method == 'POST':
        form = GatePassProductForm(request.POST)

        if 'add_product' in request.POST:
            if form.is_valid():
                gatepass_products = request.session.get('gatepass_products', [])
                product_id = form.cleaned_data['product'].id

                # Check if the product is already in the gatepass
                existing_product = next((gp for gp in gatepass_products if gp['product_id'] == product_id), None)

                if existing_product:
                    # If product exists, update its quantity and remarks
                    # existing_product['quantity'] += form.cleaned_data['quantity']
                    # existing_product['remarks'] = form.cleaned_data['remarks']
                    print('product already in gatepass')
                    messages.success(request, 'Product already in gatepass')
                else:

                    pro=get_object_or_404(Product, id=product_id)
                    unit=pro.unit.name
                    weight=int(pro.product_weight)*int(form.cleaned_data['quantity'])
                    # If product doesn't exist, add it to the session
                    gatepass_products.append({
                        'product_id': product_id,
                        'product_name': form.cleaned_data['product'].productname,
                        'quantity': form.cleaned_data['quantity'],
                        'unit':unit,
                        "weight":weight,
                        'remarks': form.cleaned_data['remarks'],
                    })
                    print('product in gatepass')

                request.session['gatepass_products'] = gatepass_products

        elif 'finalize_gatepass' in request.POST:
            if form_gatepass.is_valid():
                if not gatepass:
                    gatepass = form_gatepass.save()
                else:
                    form_gatepass.save()

                gatepass_products = request.session.pop('gatepass_products', [])
                for gp in gatepass_products:
                    product = get_object_or_404(Product, id=gp['product_id'])
                    
                    GatePassProduct.objects.create(
                        gatepass=gatepass,
                        product=product,
                       
                        quantity=gp['quantity'],
                        remarks=gp['remarks']
                    )
                return redirect('list_gatepasses')

    else:
        form = GatePassProductForm()

    gatepass_products = request.session.get('gatepass_products', [])

    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass': form_gatepass,
        'gatepass_products': gatepass_products,
        'gatepass': gatepass,
    })

from django.http import JsonResponse
@login_required
def clear_session(request):
    if 'gatepass_products' in request.session:
        del request.session['gatepass_products']
    return JsonResponse({'status': 'success'})


def edit_gatepass_product(request, product_id):
    gatepass_products = request.session.get('gatepass_products', [])
    product_to_edit = None

    for product in gatepass_products:
        if product['product_id'] == product_id:
            product_to_edit = product
            break

    if not product_to_edit:
        return redirect('create_gatepass')

    if request.method == 'POST':
        form = GatePassProductForm(request.POST)
        if form.is_valid():
            product_to_edit['product_id'] = form.cleaned_data['product'].id
            product_to_edit['product_name'] = form.cleaned_data['product'].productname
            product_to_edit['quantity'] = form.cleaned_data['quantity']
            product_to_edit['remarks'] = form.cleaned_data['remarks']

            request.session['gatepass_products'] = gatepass_products
            return redirect('create_gatepass')

    else:
        form = GatePassProductForm(initial={
            'product': product_to_edit['product_id'],
            
            'quantity': product_to_edit['quantity'],
            'remarks': product_to_edit['remarks'],
        })

    form_gatepass = GatePassForm(instance=request.session.get('gatepass_instance', None))

    return render(request, 'gatepass/edit_gatepass_product.html', {
        'form': form,
        'form_gatepass': form_gatepass
    })

def delete_gatepass_product(request, product_id):
    gatepass_products = request.session.get('gatepass_products', [])
    gatepass_products = [product for product in gatepass_products if product['product_id'] != product_id]
    request.session['gatepass_products'] = gatepass_products
    form_gatepass = GatePassForm(instance=request.session.get('gatepass_instance', None))
    return redirect('create_gatepass')


@login_required
def list_gatepasses(request):
    gatepasses = GatePass.objects.all()
    return render(request, 'gatepass/list_gatepasses.html', {'gatepasses': gatepasses})

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