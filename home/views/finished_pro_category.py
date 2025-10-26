
from django.shortcuts import render, redirect
from home.models import Finish_Product_Category
from home.forms import Finish_Product_CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.add_finish_product_category', login_url='/login/')
def add_category(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        categories=Finish_Product_Category.objects.filter(is_deleted=False)
        mydata=Finish_Product_Category.objects.filter(is_deleted=False)
        form = Finish_Product_CategoryForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Finish Product Category Added Successfully !!")
          return redirect('finished_product_category')
    else:
        mydata=Finish_Product_Category.objects.filter(is_deleted=False)
        categories=Finish_Product_Category.objects.filter(is_deleted=False)
        form = Finish_Product_CategoryForm()
    data={'form': form, 'mydata':mydata,'categories':categories}
    return render(request, 'stock_finished_product/add_category.html', data)
  else:
    return redirect('signin')
@login_required
@permission_required('home.change_finish_product_category', login_url='/login/')
def edit_category(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      categories=Finish_Product_Category.objects.filter(is_deleted=False)
      mydata=Finish_Product_Category.objects.get(id=id)
      form = Finish_Product_CategoryForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Category Updated successfully !!")
        return redirect('finished_product_category')
    else:
      mydata=Finish_Product_Category.objects.get(id=id)
      categories=Finish_Product_Category.objects.filter(is_deleted=False)
      form = Finish_Product_CategoryForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True ,'categories':categories}
  return render(request, 'stock_finished_product/add_category.html', data)


@login_required
@permission_required('home.delete_finish_product_category', login_url='/login/')

def delete_category(request,id):
 
    mydata=Finish_Product_Category.objects.get(id=id)
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Finish_Product_Category Deleted successfully !!")
    return redirect('finished_product_category')

