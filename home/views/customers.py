
from django.shortcuts import render, redirect
from home.models import Customer
from home.forms import ProductForm,Customer_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from django.db import IntegrityError

@login_required
@permission_required('home.view_customer', login_url='/login/')
def customer(request):
    customers=Customer.objects.filter(is_deleted=False)
    data={'customers':customers}
    return render(request,"customers/customer_home.html",data)   

@login_required
@permission_required('home.add_customer', login_url='/login/')
def add_customer(request):
    if request.method == 'POST':
        mydata=Customer.objects.filter(is_deleted=False)
        form = Customer_form(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Customer Added successfully !!")
          return redirect('addcustomer')
    else:
        mydata=Customer.objects.filter(is_deleted=False)
        form = Customer_form()
    data={'form': form, 'mydata':mydata}
    return render(request, 'customers/add_customer.html', data)

@login_required
@permission_required('home.change_customer', login_url='/login/')
def edit_customer(request,id):

    data={}
    if request.method == 'POST':
      mydata=Customer.objects.get(id=id)
      form = Customer_form(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Customer Updated successfully !!")
        return redirect('addcustomer')
    else:
      mydata=Customer.objects.get(id=id)
      form = Customer_form(instance=mydata)

    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'customers/add_customer.html', data)

@login_required
@permission_required('home.delete_customer', login_url='/login/')
def delete_customer(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            mydata=Customer.objects.get(id=id)
            mydata.delete()
            return JsonResponse({'success': True, 'message': 'Customer deleted successfully!'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Cannot delete this customer because it has related accounts and transactions.'})
    else:
        try:
            mydata=Customer.objects.get(id=id)
            mydata.delete()
            messages.success(request,"Customer Deleted successfully !!")
        except IntegrityError:
            messages.error(request, "Cannot delete this customer because it has related accounts and transactions.")
    return redirect('addcustomer')

