from django.contrib import messages
from django.shortcuts import render, redirect
from home.models import Fuel, Tank, Stock
from home.forms import FuelForm, TankForm, StockForm
from django.db.models import Avg,Min,Max,Count,Sum

def add_tank(request):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Tank.objects.filter(is_deleted=False)
      form = TankForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request,"Tank Added Succesfuly !!")
        return redirect('tanks')
    else:
      
      form = TankForm()
      mydata=Tank.objects.filter(is_deleted=False)

    data={'form': form, 'mydata':mydata}
    return render(request, 'equipments/add_tank.html', data)
  else:
    return redirect('signin')

def edit_tank(request,id):
  if request.user.is_authenticated: 
    data={}
    if request.method == 'POST':
      mydata=Tank.objects.get(id=id)
      form = TankForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Tank Added Succesfuly !!")
        return redirect('tanks')
    else:
        mydata=Tank.objects.get(id=id)
        form = TankForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'equipments/add_tank.html', data)
  else:
    return redirect('signin')

def delete_tank(request,id):
  if request.user.is_authenticated:
    mydata=Tank.objects.get(id=id)
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Tank Deleted Succesfuly !!")
    return redirect('tanks')
  else:
    return redirect('signin')