
from django.shortcuts import render, redirect
from home.models import Fuel, Tank
from home.forms import FuelForm, TankForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views

def add_fuel(request):
  if request.user.is_authenticated: 
    if request.method == 'POST':
        mydata=Fuel.objects.all()
        form = FuelForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Fuel Added succesfuly !!")
          return redirect('fuel')
    else:
        mydata=Fuel.objects.all()
        form = FuelForm()
    data={'form': form, 'mydata':mydata}
    return render(request, 'stock/add_fuel.html', data)
  else:
    return redirect('signin')
def edit_fuel(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Fuel.objects.get(id=id)
      form = FuelForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Fuel Updated succesfuly !!")
        return redirect('fuel')
    else:
      mydata=Fuel.objects.get(id=id)
      form = FuelForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True}
  return render(request, 'stock/add_fuel.html', data)

def delete_fuel(request,id):

 
  if request.user.is_authenticated:
    
    mydata=Fuel.objects.get(id=id)
    mydata.delete()
    messages.success(request,"Fuel Deleted succesfuly !!")
    return redirect('fuel')

  else:
    print('i m herer')
    return redirect('signin')
 
