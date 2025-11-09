
from django.shortcuts import render, redirect
from home.models import Product_Price,Finish_Product_Category,Final_Product_Price
from home.forms import Product_PriceForm,search_Product_PriceForm,Final_Product_PriceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.view_final_product_price', login_url='/login/')
def list_product_prices(request):

    prices=None
    customer=None
    prices = Final_Product_Price.objects.filter(is_deleted=False)
    region=(request.GET.get('region'))
    if region == "True":
        prices = Final_Product_Price.objects.filter(is_deleted=False, region__isnull=False)

    customer=(request.GET.get('customer'))

    if customer == "True":
        prices = Final_Product_Price.objects.filter(is_deleted=False, customer__isnull=False)

    

    data={'prices':prices,'prod':True , 'region':region , 'customer':customer , }
    return render(request, 'stock_finished_product/list_final_product_prices.html', data)

@login_required
@permission_required('home.add_product_price', login_url='/login/')
def add_product_price(request,id=''):
    if id:
        cat=Finish_Product_Category.objects.filter(is_deleted=False,id=id)
        cat1=Finish_Product_Category.objects.get(is_deleted=False,id=id)
    else:
        categoryID=int((request.GET.get('category')))
        cat=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
        cat1=Finish_Product_Category.objects.get(is_deleted=False,id=categoryID)
    if request.method == 'POST':
        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1)
        form = Product_PriceForm(request.POST,category=cat1)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Added successfully !!")
            return redirect('addproductprice', id if id else categoryID)
    else:
        
        if id:
            cat=Finish_Product_Category.objects.filter(is_deleted=False,id=id)
            cat1=Finish_Product_Category.objects.get(is_deleted=False,id=id)
        else:
            cat=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
            cat1=Finish_Product_Category.objects.get(is_deleted=False,id=categoryID)

        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1).order_by("-id")
        form = Product_PriceForm(category=cat1)
    data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
    return render(request, 'stock/add_product_prices.html', data)

@login_required
@permission_required('home.change_product_price', login_url='/login/')
def edit_product_price(request,id):
    data={}
    if request.method == 'POST':
        mydata=Product_Price.objects.get(id=id)
        categoryID=mydata.product.category.id
        form = Product_PriceForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Updated successfully !!")
            return redirect('addproductprice',categoryID)
    else:
        mydata=Product_Price.objects.get(id=id) 
        form = Product_PriceForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True,}
    return render(request, 'stock/add_product_prices.html', data)

@login_required
@permission_required('home.delete_product_price', login_url='/login/')
def delete_product_price(request,id):

    mydata=Product_Price.objects.get(id=id)
    categoryID=mydata.product.category.id
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Product Deleted successfully !!")
    return redirect('addproductprice',categoryID)


@login_required
@permission_required('home.view_product_price', login_url='/login/')
def search_product_price(request,id=''):
    if id:
        cat=Finish_Product_Category.objects.filter(is_deleted=False,id=id)
        cat1=Finish_Product_Category.objects.get(is_deleted=False,id=id)
    else:
        categoryID=int((request.GET.get('category')))
        cat=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
        cat1=Finish_Product_Category.objects.get(is_deleted=False,id=categoryID)
    if request.method == 'POST':
        form = search_Product_PriceForm(request.POST,category=cat1)
        if form.is_valid():
            product=form.cleaned_data["product"]
            customer=form.cleaned_data["customer"]
            mydata=Product_Price.objects.filter(is_deleted=False,product=product,customer=customer)
            
        data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
        return render(request, 'stock/search_product_prices.html', data)
    else:
        
        if id:
            cat=Finish_Product_Category.objects.filter(is_deleted=False,id=id)
            cat1=Finish_Product_Category.objects.get(is_deleted=False,id=id)
        else:
            cat=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
            cat1=Finish_Product_Category.objects.get(is_deleted=False,id=categoryID)

        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1).order_by("-id")
        form = search_Product_PriceForm(category=cat1)
    data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
    return render(request, 'stock/search_product_prices.html', data)


# Final Product Prices
@login_required
@permission_required('home.add_final_product_price', login_url='/login/')
def add_final_product_price(request, id=''):
    if id:
        cat = Finish_Product_Category.objects.filter(is_deleted=False, id=id)
        cat1 = Finish_Product_Category.objects.get(is_deleted=False, id=id)
    else:
        categoryID = int(request.GET.get('category'))
        cat = Finish_Product_Category.objects.filter(is_deleted=False, id=categoryID)
        cat1 = Finish_Product_Category.objects.get(is_deleted=False, id=categoryID)

    if request.method == 'POST':
        mydata = Final_Product_Price.objects.filter(
            is_deleted=False,
            product__category_id=cat1.id
        )
        form = Final_Product_PriceForm(request.POST, category=cat1)
        if form.is_valid():
            form.save()
            messages.success(request, "Final Product Price Added successfully !!")
            return redirect('addfinalproductprice', id if id else categoryID)
    else:
        if id:
            cat = Finish_Product_Category.objects.filter(is_deleted=False, id=id)
            cat1 = Finish_Product_Category.objects.get(is_deleted=False, id=id)
        else:
            cat = Finish_Product_Category.objects.filter(is_deleted=False, id=categoryID)
            cat1 = Finish_Product_Category.objects.get(is_deleted=False, id=categoryID)

        mydata = Final_Product_Price.objects.filter(
            is_deleted=False,
            product__category_id=cat1.id
        ).order_by("-id")

        print('category in views', mydata)
        form = Final_Product_PriceForm(category=cat1)

    data = {
        'form': form,
        'mydata': mydata,
        'categories': cat,
        'prod': True,
        'category': cat1
    }
    return render(request, 'stock_finished_product/add_final_product_prices.html', data)

@login_required
@permission_required('home.add_final_product_price', login_url='/login/')
def add_final_product_pricemain(request):
    if request.method == 'POST':
        mydata = Final_Product_Price.objects.filter(
            is_deleted=False,
        )
        form = Final_Product_PriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Final Product Price Added successfully !!")
            return redirect('addfinalproductpricemain')
    else:
        
        mydata = Final_Product_Price.objects.filter(
            is_deleted=False,
        ).order_by("-id")

        print('category in views', mydata)

        for i in mydata:
            print(i.price_list)
        form = Final_Product_PriceForm()

    data = {
        'form': form,
        'mydata': mydata,
        'prod': True,
      
    }
    return render(request, 'stock_finished_product/add_final_product_prices.html', data)

@login_required
@permission_required('home.add_final_product_price', login_url='/login/')
def edit_final_product_pricemain(request, id):
    if request.method == 'POST':
        # get raw string values
        id = request.POST['pricelist']
        product_id = request.POST['product']
        price = request.POST['price']

        # convert to correct types
        id = int(id)  
        product_id = int(product_id)  
        price = float(price)  

        print(type(id),'list')       # <class 'int'>
        print(type(product_id),'pro') # <class 'int'>
        print(type(price),'price')    # <class 'float'>

        print(id, product_id, price)

        # ✅ Update record instead of re-creating
        data=Final_Product_Price.objects.filter(price_list_id=id, product_id=product_id).update(
            product_id=product_id,
            price=price)
        print(data)
        return redirect('pricelistdetail' , id=id )

@login_required
@permission_required('home.change_product_price', login_url='/login/')
def edit_final_product_price(request,id):
    print("dfsdfdsfs")
    data={}
    if request.method == 'POST':
        mydata=Final_Product_Price.objects.get(id=id)
        categoryID=mydata.product.category.id
        form = Final_Product_PriceForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Updated successfully !!")
            return redirect('addfinalproductprice',categoryID)
    else:
        mydata=Final_Product_Price.objects.get(id=id) 
        form = Final_Product_PriceForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True,}
    return render(request, 'stock_finished_product/add_final_product_prices.html', data)


@login_required
@permission_required('home.delete_product_price', login_url='/login/')
def delete_final_product_price(request,id):

    mydata=Final_Product_Price.objects.get(id=id)
    categoryID=mydata.product.category.id
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Product Deleted Successfully !!")
    return redirect('addfinalproductprice',categoryID)