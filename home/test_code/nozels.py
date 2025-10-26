from django.contrib import messages
from django.shortcuts import redirect, render
from home.forms import NozelForm
from home.models import Nozel

# Create your views here.

def nozel(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      mydata = Nozel.objects.filter(is_deleted=False)
      form = NozelForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request,"Nozel Added Succesfuly !!")
        return redirect('nozels')
    else:
      form = NozelForm()
      mydata = Nozel.objects.filter(is_deleted=False)
  else:
    return redirect('signin')
  data={'mydata':mydata,'form':form}
  return render(request,'equipments/nozels.html',data)

def edit_nozel(request,id):
  if request.user.is_authenticated: 
    data={}
    if request.method == 'POST':
      mydata=Nozel.objects.get(id=id)
      form = NozelForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Nozel Updated Succesfuly !!")
        return redirect('nozels')
    else:
        mydata=Nozel.objects.get(id=id)
        form = NozelForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'equipments/nozels.html', data)
  else:
    return redirect('signin')
  
def delete_nozel(request,id):
  if request.user.is_authenticated:
    try:
      mydata=Nozel.objects.get(id=id)
      mydata.is_deleted=True
      mydata.save()
      messages.success(request,"Nozel Deleted Succesfuly !!")
      return redirect('nozels')
    except:
      pass
  else:
    return redirect('signin')
  
