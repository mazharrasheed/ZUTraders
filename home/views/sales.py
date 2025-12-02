# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Sales_Receipt_ProductForm,Sales_ReceiptForm,Sales_Cash_Receipt_ProductForm,Sales_Cash_ReceiptForm
from ..models import Sales_Receipt, Sales_Receipt_Product,Product_Price,Transaction,Account,Customer,Final_Product,Final_Product_Price
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum
from collections import defaultdict
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def get_final_product_stock(request,id):
    print('fdfsfdf')
    product_price=None
    price_list=None
    customer=None
    customer_id = request.GET.get('customer')
    print('customer from getstock ',customer_id)
    product=Final_Product.objects.get(id=id)
    stock_qty=product.get_current_stock()
    
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
        print(customer.price_list.name)
        product_price=product.get_price_for_customer(customer=customer)
        price_list=customer.price_list.name

    print('from get stock',product_price)
    print(stock_qty)
    print(id,stock_qty)
    return JsonResponse({'success': True,'stock':stock_qty,'price':product_price,'price_list':price_list})


@login_required
@permission_required('home.view_sales_receipt', login_url='/login/')
def list_sales(request):
    salereceipt_items_pro = {}
    total_amount = {}
    salereceipts = []
    if request.method== 'GET':
        customer = request.GET.get('customer')
        cash = request.GET.get('cash')
        print(customer,cash)
        if customer:
            salereceipts = Sales_Receipt.objects.filter(is_cash=False)
        elif cash == "True":
            salereceipts = Sales_Receipt.objects.filter(is_cash=True)
        else:
            salereceipts = Sales_Receipt.objects.all()
    else:
        salereceipts = Sales_Receipt.objects.all()
    for x in salereceipts:
        # Count the number of products for each sale receipt
        print(x.transaction_ref)
        salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
        # Get products for the sale receipt and aggregate the amount
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
        total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))

    total_sale = sum(item['amount__sum'] or 0 for item in total_amount.values())

    # Prepare JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
        'total_sale': total_sale,
      })

    # Return HTML response for standard requests
    return render(request, 'sale/list_sales.html', {
        'salereceipts': salereceipts,
        'salereceipt_items_pro': salereceipt_items_pro,
        'total_amount': total_amount,
        'total_sale': total_sale,
        'customer': customer,
        'cash': cash,
    })

@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def salereceipt(request):
    form = Sales_Receipt_ProductForm()
    form_salereceipt=Sales_ReceiptForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_salereceipt':form_salereceipt,
    })

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from ..forms import Sales_ReceiptForm, Sales_Receipt_ProductForm
from ..models import Sales_Receipt, Sales_Receipt_Product, Final_Product, Final_Product_Price
from django.db import transaction
@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')


def create_salereceipt(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:
            form_salereceipt = Sales_ReceiptForm(request.POST)
            products = request.POST.getlist('products[]')

            if form_salereceipt.is_valid() and products:
                try:
                    with transaction.atomic():  # 👈 Everything inside will rollback on error
                        salercpt = form_salereceipt.save(commit=False)
                        salercpt.created_by = request.user
                        salercpt.save()

                        customer = form_salereceipt.cleaned_data.get('customer_name')
                        region = form_salereceipt.cleaned_data.get('region')

                        for product_data in products:
                            product_id, quantity = product_data.split(':')
                            product = get_object_or_404(Final_Product, id=product_id)

                            unit_price_obj = None
                            if customer:
                                customer_obj = Customer.objects.get(coname=customer)
                                unit_price =  product.get_price_for_customer(customer_obj)
                                print(unit_price)
                            
                            if not unit_price:
                                raise ValueError(f'No price defined for product {product.productname}')  

                            quantity = int(quantity)
                            unit_price = float(unit_price)
                            amount = unit_price * quantity

                            Sales_Receipt_Product.objects.create(
                                salereceipt=salercpt,
                                product=product,
                                quantity=quantity,
                                unit_price=unit_price,
                                amount=amount
                            )
                            product.change_status()

                        return JsonResponse({'success': True, 'redirect_url': '/list-sales?customer=True'})
                except Exception as e:
                    return JsonResponse({'success': False, 'errors': str(e)})
            else:
                return JsonResponse({'success': False, 'errors': form_salereceipt.errors.as_json()})

    else:
        form = Sales_Receipt_ProductForm()
        form_salereceipt = Sales_ReceiptForm()

    return render(request, 'sale/create_salereceipt.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
    })



@login_required
@permission_required('home.change_sales_receipt', login_url='/login/')
def edit_salereceipt(request, id):
    salereceipt = get_object_or_404(Sales_Receipt, pk=id)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:
            form_salereceipt = Sales_ReceiptForm(request.POST, instance=salereceipt)
            products = request.POST.getlist('products[]')

            if form_salereceipt.is_valid() and products:
                salereceipt = form_salereceipt.save(commit=False)
                salereceipt.created_by = request.user
                salereceipt.save()

                customer = form_salereceipt.cleaned_data.get('customer_name')
                

                # clear old products
                salereceipt.sales_receipt_products.all().delete()

                for product_data in products:
                    try:
                        product_id, quantity = product_data.split(':')
                        product = get_object_or_404(Final_Product, id=product_id)

                        # Find price (customer)
                        unit_price_obj = None
                        if customer:
                            customer_obj = Customer.objects.get(coname=customer)
                            unit_price=product.get_price_for_customer(customer_obj)
                        
                        if not unit_price:
                            return JsonResponse({
                                'success': False,
                                'errors': f'No price defined for product {product.productname}'
                            })

                        quantity = int(quantity)
                        unit_price = float(unit_price)
                        amount = unit_price * quantity

                        Sales_Receipt_Product.objects.create(
                            salereceipt=salereceipt,
                            product=product,
                            quantity=quantity,
                            unit_price=unit_price,
                            amount=amount
                        )

                        product.change_status()

                    except Exception as e:
                        return JsonResponse({'success': False, 'errors': str(e)})

                return JsonResponse({'success': True, 'redirect_url': '/list-sales?customer=True'})
            else:
                return JsonResponse({'success': False, 'errors': form_salereceipt.errors.as_json()})

    else:
        form = Sales_Receipt_ProductForm()
        form_salereceipt = Sales_ReceiptForm(instance=salereceipt)

    return render(request, 'sale/edit_salereceipt.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })


@login_required
@permission_required('home.delete_sales_receipt', login_url='/login/')
def delete_salereceipt_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(Sales_Receipt_Product, id=id)
        salereceipt_id = request.POST.get('salereceipt_id')
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def create_cash_salereceipt(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:  # Finalize the purchase note
            form_salereceipt = Sales_Cash_ReceiptForm(request.POST)
            products = request.POST.getlist('products[]')
            if form_salereceipt.is_valid() and products:
                salercpt = form_salereceipt.save(commit=False)
                salercpt.created_by = request.user
                salercpt.is_cash = True
                salercpt.save()
                for product_data in products:
                    product_id, quantity , unit_price, amount= product_data.split(':')
                    Sales_Receipt_Product.objects.create(
                        salereceipt=salercpt,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        amount=amount
                    )
                    Final_Product.objects.get(id=product_id).change_status()
                return JsonResponse({'success': True, 'redirect_url': '/list-sales?cash=True'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = Sales_Cash_Receipt_ProductForm()
        form_salereceipt = Sales_Cash_ReceiptForm()
    return render(request, 'sale/create_cash_salereceipt.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
    })

@login_required
@permission_required('home.change_sales_receipt', login_url='/login/')
def edit_cash_salereceipt(request,id):
    salercpt = get_object_or_404(Sales_Receipt, id=id)
    products = Sales_Receipt_Product.objects.filter(salereceipt=salercpt.id)
    if request.method == 'POST':
        form = Sales_Cash_ReceiptForm(request.POST, instance=salercpt)
        if form.is_valid():
            grn = form.save()
            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')
            # Delete removed products
            Sales_Receipt_Product.objects.filter(salereceipt=salercpt, product__id__in=deleted_products).delete()
            product_quantities = defaultdict(int)
            for product_info in product_data:
                try:
                    product_id, quantity,unit_price,amount = product_info.split(':')
                    product_quantities[product_id] += int(quantity)
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Invalid product data.'})

            for product_id, total_quantity in product_quantities.items():

                try:
                    product_id, quantity,unit_price,amount = product_info.split(':')
                    product_instance = Final_Product.objects.get(id=product_id)
                    print("product id :",product_id, "qty:",total_quantity,unit_price,amount)
                    product, created = Sales_Receipt_Product.objects.update_or_create(
                        salereceipt=salercpt,
                        product=product_instance,
                        defaults={
                            'quantity': total_quantity,
                            'unit_price': float(unit_price),
                            'amount': float(amount),
                        }
                    )
                    Final_Product.objects.get(id=product_id).change_status()
                except Final_Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with ID {product_id} does not exist.'})

            return JsonResponse({'success': True, 'redirect_url': '/list-sales?cash=True'})

        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    context = {
        'salereceipt': salercpt,
        'products': products,
        'form_salereceipt': Sales_Cash_ReceiptForm(instance=salercpt),
        'form': Sales_Cash_Receipt_ProductForm(),
    }
    return render(request, 'sale/edit_cash_salereceipt.html', context)


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def cancel_salereceipt(request,id):
    # salereceipt_id=(request.GET.get('salereceipt_id'))
    salereceipt=get_object_or_404(Sales_Receipt,id=id)
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    #
    if salereceipt_products:
        for item in salereceipt_products:
            item.delete()
    salereceipt.delete()
    messages.success(request, "Your sale receipt canceled !")
    return redirect('list_sales')

@login_required
@permission_required('home.delete_sales_receipt', login_url='/login/')
def delete_salereceipt(request, id):
    product_list=[]
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        salereceipt = get_object_or_404(Sales_Receipt, id=id)
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
        if salereceipt.make_transaction==True:
            return JsonResponse({'success': False, 'message': 'Sale receipt has a related transaction can not be deleted!'})
        else:
            if salereceipt_products:
                for pro in salereceipt_products:
                    product_list.append(pro.product)
                salereceipt_products.delete()  # Bulk delete all related products
                for i in product_list:
                    i.change_status()
            salereceipt.delete()
            return JsonResponse({'success': True, 'message': 'Sale receipt deleted successfully!'})
    # For non-AJAX requests, handle as usual
    salereceipt = get_object_or_404(Sales_Receipt, id=id)
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    if salereceipt_products:
        for pro in salereceipt_products:
            product_list.append(pro.product)
        salereceipt_products.delete()  # Bulk delete all related products
        # change stust of product after deletion of sale receipt
        for i in product_list:
            i.change_status()
        salereceipt_products.delete()  # Bulk delete all related products
    salereceipt.delete()
    messages.success(request, "Sale receipt deleted successfully!")
    return redirect('list_salereceipts')

@login_required
@permission_required('home.view_sales_receipt', login_url='/login/')
def print_salereceipt(request, salereceipt_id):
    # Fetch the salereceipt instance by ID
    salereceipt = get_object_or_404(Sales_Receipt, id=salereceipt_id)
    # Fetch all products associated with this salereceipt
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    total_amount=salereceipt_products.aggregate(Sum('amount'))
    return render(request, 'sale/print_salereceipt.html', {
        'salereceipt': salereceipt,
        'salereceipt_products': salereceipt_products,
        'total_amount':total_amount

    })

def make_transaction1(request,id):

    salereceipt_items_pro = {}
    total_amount = {}
    salereceipt = get_object_or_404(Sales_Receipt, id=id)
    print(salereceipt.customer_name,"ddd")
    salereceipts = Sales_Receipt.objects.all()

    for x in salereceipts:
        # Count the number of products for each sale receipt
        salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
        # Get products for the sale receipt and aggregate the amount
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
        total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))
    coname=salereceipt.customer_name
    print(coname,"eee")
    customer=Customer.objects.get(coname=coname, is_deleted=False)
    debit_account=Account.objects.get(customer=customer.id,is_deleted=False)
    credit_account=Account.objects.get(account_type="Revenue",name="Sales",is_deleted=False)
    amt=total_amount[id]
    print(amt)
    amount=amt['amount__sum']
    transaction=Transaction(description=f' sales receipt id = {salereceipt.id}',debit_account=debit_account,credit_account=credit_account,amount=amount,date=salereceipt.date_created)
    transaction.made_by=request.user
    transaction.save()
    salereceipt.make_transaction=True
    salereceipt.save()
    salereceipts = Sales_Receipt.objects.all()
    messages.success(request, "Transaction added successfully!")

    return redirect('list_sales')

    # return render(request, 'sale/list_sales.html', {
    #     'salereceipts': salereceipts,
    #     'salereceipt_items_pro': salereceipt_items_pro,
    #     'total_amount': total_amount
    # })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from ..models import Sales_Receipt, Sales_Receipt_Product, Customer, Account, Transaction

def make_transaction(request, id):
    if request.method == "POST":
        salereceipt_items_pro = {}
        total_amount = {}
        salereceipt = get_object_or_404(Sales_Receipt, id=id)
        salereceipts = Sales_Receipt.objects.all()

        for x in salereceipts:
            salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
            salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
            total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))

        customer_name = salereceipt.customer_name
        customer = Customer.objects.get(coname=customer_name, is_deleted=False)
        debit_account = Account.objects.get(customer=customer.id, is_deleted=False)
        credit_account = Account.objects.get(account_type="Revenue", name="Sales", is_deleted=False)

        amt = total_amount[id]
        amount = amt['amount__sum'] if amt['amount__sum'] else 0

        transaction = Transaction(
            description=f'Sales receipt id = {salereceipt.id}',
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            date=salereceipt.date_created,
            transaction_type="Sales",
            transaction_ref="TRX"+str(salereceipt.id)+str(datetime.now().strftime("%Y%m%d%H%M%S")),
            made_by=request.user
        )
        transaction.save()

        salereceipt.make_transaction = True
        salereceipt.transaction_ref = transaction.transaction_ref
        salereceipt.save()

        # Return JSON response for AJAX
        return JsonResponse({
            "status": "success",
            "message": "Transaction added successfully!",
            "transaction_id": transaction.id,
            "transaction_ref": transaction.transaction_ref,
            "amount": amount
        })

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
