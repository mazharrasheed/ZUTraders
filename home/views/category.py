
from django.shortcuts import render, redirect,get_object_or_404
from home.models import Category
from home.forms import CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.db import IntegrityError

@login_required
@permission_required('home.add_category', login_url='/login/')
def add_category(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        categories=Category.objects.filter(is_deleted=False)
        mydata=Category.objects.filter(is_deleted=False)
        form = CategoryForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Category Added successfully !!")
          return redirect('category')
    else:
        mydata=Category.objects.filter(is_deleted=False)
        categories=Category.objects.filter(is_deleted=False)
        form = CategoryForm()
    data={'form': form, 'mydata':mydata,'categories':categories}
    return render(request, 'stock/add_category.html', data)
  else:
    return redirect('signin')
@login_required
@permission_required('home.change_category', login_url='/login/')
def edit_category(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      categories=Category.objects.filter(is_deleted=False)
      mydata=Category.objects.get(id=id)
      form = CategoryForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Category Updated successfully !!")
        return redirect('category')
    else:
      mydata=Category.objects.get(id=id)
      categories=Category.objects.filter(is_deleted=False)
      form = CategoryForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True ,'categories':categories}
  return render(request, 'stock/add_category.html', data)

from django.db import IntegrityError
@login_required
@permission_required('home.view_product', login_url='/login/')

def delete_category(request, id):
    try:
        mydata = get_object_or_404(Category, id=id)
        mydata.delete()
        messages.success(request, "Category deleted successfully!")
    except IntegrityError:
        messages.error(request, "Cannot delete this category because it has related products.")
    return redirect('category')

