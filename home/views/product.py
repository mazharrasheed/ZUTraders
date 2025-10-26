
from django.shortcuts import render, redirect
from home.models import Product,Category,Final_Product
from home.forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError


@login_required
@permission_required('home.view_store', login_url='/login/')

def store(request):
   return render(request,"store/index.html")   
   
@login_required
@permission_required('home.view_product', login_url='/login/')
def products(request):
    category_selected=False
    categoryID=(request.GET.get('category'))
    if categoryID:
        categories=Category.objects.filter(is_deleted=False,id=categoryID)
        category_selected=True
        products=Product.objects.filter(category=categoryID,is_deleted=False)
        # products=Product.objects.filter(is_deleted=False)
    else:
        categories=Category.objects.filter(is_deleted=False)
        products=Product.objects.filter(is_deleted=False).order_by('category')
        messages.success(request,"Items Loaded successfully !!")
    data={'products':products,'categories':categories,'category_selected':category_selected}
    return render(request,"stock/products_home.html",data)   

@login_required
# @permission_required('home.add_sales_product', login_url='/login/')
def add_product(request,id=''):
  if id:
    categories=Category.objects.filter(is_deleted=False,id=id)
  else:

    categoryID=int((request.GET.get('category')))
    categories=Category.objects.filter(is_deleted=False,id=categoryID)

    
  if request.method == 'POST':
      mydata=Product.objects.filter(is_deleted=False)
      form = ProductForm(request.POST,request.FILES)
      if form.is_valid():
        form.save()
        messages.success(request,"Product Added successfully !!")
        if id:
          return redirect('addproduct1',id)
        else:
          return redirect('addproduct1',categoryID)
  else:
      
      if id:
        cat=Category.objects.get(is_deleted=False,id=id)
      else:
        cat=Category.objects.get(is_deleted=False,id=categoryID)
      mydata=Product.objects.filter(is_deleted=False,category=cat).order_by("-id")
      form = ProductForm(initial={'category': cat})
  data={'form': form, 'mydata':mydata,'categories':categories,'prod':True}
  return render(request, 'stock/add_product.html', data)

@login_required
# @permission_required('home.add_sales_product', login_url='/login/')
def add_product1(request):
  if request.method == 'POST':
      mydata=Product.objects.filter(is_deleted=False)
      form = ProductForm(request.POST,request.FILES)
      if form.is_valid():
        form.save()
        messages.success(request,"Product Added successfully !!")
        return redirect('addproduct2')
  else:
      mydata=Product.objects.filter(is_deleted=False).order_by("-id")
      form = ProductForm()
  data={'form': form, 'mydata':mydata,'prod':True}
  return render(request, 'stock/add_product.html', data)

@login_required
@permission_required('home.change_sales_product', login_url='/login/')
def edit_product(request,id):
  data={}
  if request.method == 'POST':
    mydata=Product.objects.get(id=id)
    categoryID=mydata.category.id
    form = ProductForm(request.POST,request.FILES,instance=mydata)
    if form.is_valid():
      form.save()
      messages.success(request,"Product Updated successfully !!")
      return redirect('addproduct1',categoryID)
  else:
    mydata=Product.objects.get(id=id) 
    form = ProductForm(instance=mydata)
  data={'form': form, 'mydata':mydata,'update':True,}
  return render(request, 'stock/add_product.html', data)


@login_required
@permission_required('home.delete_product', login_url='/login/')

def delete_product(request,id):
  print(request.path)
  try:
    mydata=get_object_or_404(Product, id=id)
    categoryID=mydata.category.id
    mydata.delete()
    messages.success(request,"Product Deleted successfully !!")
  except IntegrityError:
      messages.error(request, "Cannot delete this product because it used in store notes")
  return redirect('product')

from ..models import Inventory

# def inventory(request):

#   inventory = Inventory.objects.all()
#   # print(f"Product: {inventory.product.productname}, Stock: {inventory.quantity} units")
#   print(inventory)
#   data={ 'mydata':inventory}
#   return render(request, 'stock/inventory.html', data)


# def inventory(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     current_stock = product.get_current_stock()
#     return render(request, 'stock/inventory.html', {'product': product, 'current_stock': current_stock})


def inventory(request):
    # Fetch all products
    products = Final_Product.objects.all()
    # Calculate stock for each product
    product_stock = []
    for product in products:
        current_stock = product.get_current_stock()
        product.change_status()
        product_stock.append({'product': product, 'current_stock': current_stock})
    return render(request, 'stock/inventory.html', {'mydata': product_stock})