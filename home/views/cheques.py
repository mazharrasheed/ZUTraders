
from django.shortcuts import render, redirect
from home.models import Cheque
from home.forms import Cheques_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone

@login_required
@permission_required('home.view_cheque', login_url='/login/')
def cheque(request):
    cheques=Cheque.objects.filter(is_deleted=False)
    for cheque in cheques:
        if cheque.cheque_date:  
            cheque_late = date.today() >= cheque.cheque_date
            print(date.today(),cheque_late)
            if cheque_late :
                cheque.highlight_red= True
                print(cheque.highlight_red,'33333')
            else:
                cheque.highlight_red= False
                print(cheque.highlight_red,'2222')
        else:
            cheque.highlight_red = False

        print(cheque.highlight_red)
    data={'cheques':cheques}
    return render(request,"cheques/cheque_home.html",data)   

@login_required
@permission_required('home.add_cheque', login_url='/login/')
def add_cheque(request):
    if request.method == 'POST':
        mydata=Cheque.objects.filter(is_deleted=False)
        form = Cheques_form(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Cheque Added successfully !!")
          return redirect('addcheque')
    else:
        mydata=Cheque.objects.filter(is_deleted=False)
        form = Cheques_form()
    data={'form': form, 'mydata':mydata}
    return render(request, 'cheques/add_cheque.html', data)

@login_required
@permission_required('home.change_cheque', login_url='/login/')
def edit_cheque(request,id):
    data={}
    if request.method == 'POST':
      mydata=Cheque.objects.get(id=id)
      form = Cheques_form(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Cheque Updated successfully !!")
        return redirect('addcheque')
    else:
      mydata=Cheque.objects.get(id=id)
      form = Cheques_form(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'cheques/add_cheque.html', data)

@login_required
@permission_required('home.delete_cheque', login_url='/login/')
def delete_cheque(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        mydata=Cheque.objects.get(id=id)
        mydata.is_deleted=True
        mydata.save()
        return JsonResponse({'success': True, 'message': 'Cheque deleted successfully!'})
    else:
        mydata=Cheque.objects.get(id=id)
        mydata.is_deleted=True
        mydata.save()
        messages.success(request,"Cheque Deleted successfully !!")
        return redirect('addcheque')
 
