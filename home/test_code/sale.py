from django.contrib import messages
from django.shortcuts import render, redirect
from home.models import Sale,Nozel,Tank,Stock,Account
from home.forms import SaleForm
from django.db.models import Avg,Min,Max,Count,Sum

def add_sale(request):
  
  if request.user.is_authenticated: 
    if request.method == 'POST':
      selected_noz=(request.GET.get('nozzle'))
      SaleForm.selected_nozzle['nzid']=selected_noz
      sales = Sale.objects.filter(is_deleted=False)
      form = SaleForm(request.POST)
      qty=int(request.POST['present_reading'])-int(request.POST['previous_reading'] )
      if qty <1:
        messages.warning(request,"Check! Invalid Second Reading , Add More Than First Reading !!!")
        return redirect('sale')
      id=int(request.POST['nozel'])
      stk=Nozel.objects.get(id=id).tank.in_stock
      if qty > stk:
        messages.warning(request,"Check! Insufficient Stock , Sale is More Than Stock, Try Again !!!")
        return redirect('sale')
      else:
        if form.is_valid(): 
          form.save()
          messages.success(request,"Sale Added Succesfuly !!")
          return redirect('sale')
    else:

      selected_noz=(request.GET.get('nozzle'))
      SaleForm.selected_nozzle['nzid']=selected_noz
      form = SaleForm()
      sales = Sale.objects.filter(is_deleted=False)
      nozel = Nozel.objects.filter(is_deleted=False)
    return render(request, 'sale/add_sale.html', {'form': form ,'mydata':sales,'nozzles':nozel})
  else:
    return redirect('signin')

def add_sale_select_nozel(request):

  if request.user.is_authenticated: 
    if request.method == 'POST':
      sales = Sale.objects.filter(is_deleted=False)
      form = SaleForm(request.POST)
      qty=int(request.POST['present_reading'])-int(request.POST['previous_reading'] )
      if qty <1:
        messages.warning(request,"Check! Invalid Second Reading , Add More Than First Reading !!!")
        return redirect('sale')
      id=int(request.POST['nozel'])
      stk=Nozel.objects.get(id=id).tank.in_stock
      if qty > stk:
        messages.warning(request,"Check! Insufficient Stock , Sale is More Than Stock, Try Again !!!")
        return redirect('sale')
      else:
        if form.is_valid(): 
          form.save()
          messages.success(request,"Sale Added Succesfuly !!")
          return redirect('sale')
    else:
      nozzleID=(request.GET.get('nozzle'))
      SaleForm.is_nozzle=True
      selected_nozzle=""
      form = SaleForm()
      sales = Sale.objects.filter(is_deleted=False)
    return render(request, 'sale/add_sale.html', {'form': form ,'mydata':sales})
  else:
    return redirect('signin')

def edit_sale(request,id):
   
  if request.user.is_authenticated: 
    data={}
    if request.method == 'POST':
      sale = Sale.objects.get(id=id)
      form = SaleForm(request.POST,instance=sale)
      if form.is_valid():
        Sale.update=True
        form.save()
        messages.success(request,"Sale Updated Succesfuly !!")
        return redirect('sale')
    else:
      sale = Sale.objects.get(id=id)
      form = SaleForm(instance=sale)
    data={'form': form, 'mydata':sale,'update':True}
    return render(request, 'sale/add_sale.html', data)
  else:
    return redirect('signin')

def delete_sale(request,id):
  if request.user.is_authenticated:

      mydata=Sale.objects.get(id=id)
      mydata.nozel.tank.in_stock += mydata.quantity
      mydata.nozel.tank.save()
      mydata.is_deleted=True
      Sale.isdelete=True
      mydata.save()
      Sale.isdelete=False
      messages.success(request,"Sales Deleted Succesfuly !!")
      return redirect('sale')
  else:
    return redirect('signin')


