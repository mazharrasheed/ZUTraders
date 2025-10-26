
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import Create_User_Form


@login_required
@permission_required('auth.add_user',login_url='/login/')
def list_users(request):
  users=User.objects.all()
  data={'users':users}
  return render(request,'users/list_users.html',data)

@login_required
@permission_required('auth.add_user',login_url='/login/')
def create_user(request):
  if request.method=="POST":
    form=Create_User_Form(request.POST)
    if form.is_valid():
      form.save()
      user = form.save(commit=False)
      user.is_staff=False
      user.save()
      # adding user in to a group on user creation
      group = form.cleaned_data['group']
      user.groups.add(group)
      form = Create_User_Form()
      messages.success(request,"User created succesfully !!")
      return redirect('createuser')
  else:
    form=Create_User_Form()
  data={'form':form}
  return render(request,'users/create_user.html',data)


@login_required
@permission_required('auth.add_user',login_url='/login/')
def user_details(request,id):

  issued=False
  requested=False

  user=User.objects.get(id=id)
  issue_request=user.requests_created.all()
  request_issued=user.created_issue_notes.all()

  if request.GET.get('Issue_Requests'):
  # issue_request=user.requests_created.all()
    request_data=issue_request
    requested=True

  elif request.GET.get('Issue_Notes'):
    # request_issued=user.created_issue_notes.all()
    request_data=request_issued
    issued=True

    # print(request_data)

    # for req in request_data:
    #   print(f"Issue Request ID: {req.id}, Date: {req.date_created}, Project: {req.project}")

    #   # Access products and quantities
    #   for item in req.store_issue_products.all():
    #       print(f" - Product: {item.product.productname}, Quantity: {item.quantity}")


  # for req in issue_request:
  #   print(f"Issue Request ID: {req.id}, Date: {req.date_created}, Project: {req.project}")

  #   # Access products and quantities
  #   for item in req.store_issue_request_product_set.all():
  #       print(f" - Product: {item.product.productname}, Quantity: {item.quantity}")

  data={'request_data':request_data,'issued':issued,'requested':requested}
  return render(request,'users/user_details.html',data)
