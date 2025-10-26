from django.contrib import messages
from django.shortcuts import render, redirect
from home.models import Fuel, Tank, Stock
from home.forms import FuelForm, TankForm, StockForm
from django.db.models import Avg,Min,Max,Count,Sum

def add_stock(request):
  if request.user.is_authenticated: 
    if request.method == 'POST':
      stocks = Stock.objects.filter(is_deleted=False)
      form = StockForm(request.POST)
      qty=int(request.POST['quantity']) 
      id=int(request.POST['tank'])
      cap=(Tank.objects.get(id=id).capacity)-((Tank.objects.get(id=id).in_stock))
      if qty > cap:
        messages.warning(request," Tank is full,Can Not Add More Than Cpacity, Try Again !!!")
        return redirect('stock')
      else:
        if form.is_valid():    
          form.save()
          messages.success(request,"Stock Added Succesfuly !!")
          return redirect('stock')
    else:
      form = StockForm()
      stocks = Stock.objects.filter(is_deleted=False)
      stocks = Stock.objects.filter(is_deleted=False)
      inventory_data = {}
      for stock in stocks:
        key = (stock.tank.name,stock.fuel, stock.price)
        if key in inventory_data:
          inventory_data[key] += stock.quantity
        else:
          inventory_data[key] = stock.quantity
    return render(request, 'stock/add_stock.html', {'form': form ,'stocks':stocks,'inventory_data': inventory_data})
  else:
    return redirect('signin')

def edit_stock(request,id): 
  if request.user.is_authenticated: 
    data={}
    if request.method == 'POST':
      stock = Stock.objects.get(id=id)
      old_qty=stock.quantity
      form = StockForm(request.POST,instance=stock)
      qty=int(request.POST['quantity']) 
      id=int(request.POST['tank'])
      cap=(Tank.objects.get(id=id).capacity)-((Tank.objects.get(id=id).in_stock))
      if qty > cap:
        messages.warning(request," Tank is full,Can not Add More Than Cpacity, Try Again !!!")
        return redirect('stock')
      else:
        if form.is_valid():
          Stock.update=True
          Stock.old_qty=old_qty
          form.save()
          messages.success(request,"Stock Updated Succesfuly !!")
          return redirect('stock')
    else:
      stock = Stock.objects.get(id=id)
      form = StockForm(instance=stock)
    data={'form': form, 'stock':stock,'update':True}
    return render(request, 'stock/add_stock.html', data)
  else:
    return redirect('signin')

def delete_stock(request,id):
  if request.user.is_authenticated:
      mydata=Stock.objects.get(id=id)
      mydata.tank.in_stock -= mydata.quantity
      mydata.tank.save()
      mydata.is_deleted=True
      Stock.isdelete=True
      mydata.save()
      Stock.isdelete=False
      messages.success(request,"Stock Deleted Succesfuly !!")
      return redirect('stock')
  else:
    return redirect('signin')
