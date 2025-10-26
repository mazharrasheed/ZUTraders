from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from ..forms import Add_Blog, AdminUserPrifoleForm, EditUserPrifoleForm, Sign_Up
from ..models import Blog

# Create your views here.

def index(request):
  # if request.user.is_authenticated:
  myblog=Blog.objects.all()
  # else:
    # return redirect('signin')
  data={'myblog':myblog}
  return render(request,'index.html',data)

def detail(request,id):

  myblog=Blog.objects.get(id=id)
  data={'myblog':myblog}
  return render(request,'detail.html',data)

def edit_data(request,id): 
    data={}
    if request.method=='POST':
        pst=Blog.objects.get(id=id)
        form=Add_Blog(request.POST,instance=pst)
        if form.is_valid():
          form.save()
          messages.success(request,"Blog Updated succesfuly !!")
          # return redirect('dashboard')
    else:
        pst=Blog.objects.get(id=id)
        form=Add_Blog(instance=pst)
    data={'form':form,'pst':pst}
    return render(request,'update.html',data)
'''
def delete_data(request,id):
  print("dfsdfdsf")
  if request.user.is_authenticated:
    user=request.user
    perm=User.get_user_permissions(user)
    for pm in perm:
      if pm=="home.delete_blog":
        pst=Blog.objects.get(id=id)
        pst.delete()
    return redirect('dashboard')
  else:
    return redirect('signin')'''

def delete_data(request,id):
  if request.user.is_authenticated:
    if request.method=='POST':
      pst=Blog.objects.get(id=id)
      pst.delete()
      return redirect('dashboard')
    else:
      messages.success(request, "You are not authorized to delete")
      return redirect('dashboard')
  else:
    return redirect('signin')

def post_blog(request):
  if request.user.is_authenticated:
    if request.method=='POST':
      form=Add_Blog(request.POST)
      title=request.POST['title']
      desc=request.POST['description']
      loginuser=request.user
      pst=Blog(title=title,description=desc,user=loginuser)
      pst.save()
      messages.success(request,"Blog posted succesfuly !!")
      # return redirect('dashboard')
    else:
      form=Add_Blog()
    data={'form':form}
    return render(request,'postblog.html',data)
  else:
    return redirect('signin')

def dashboard(request):
  if request.user.is_authenticated:

    if request.user.is_superuser==True:
      myblog=Blog.objects.all()
      data={'myblog':myblog}
      pass
    else:
      user=request.user
      myblog=Blog.objects.filter(user=user)
      gps=user.groups.all()
      data={'myblog':myblog,'groups':gps}
    return render(request,'dashboard.html',data)
  else:
    return redirect('signin')

def sign_up(request):
  if request.method=="POST":
    form=Sign_Up(request.POST)
    if form.is_valid():
      form.save()
      user = form.save()
      # adding user in to a group on Signup
      group = Group.objects.get(name='author')
      user.groups.add(group)
      form = Sign_Up()
      messages.success(request,"account created succesfuly !!")
      return redirect('signup')
  else:
    form=Sign_Up()
  data={'form':form}
  return render(request,'signup.html',data)

def log_out(request):

  logout(request)
  return redirect('signin')

def sign_in(request):
  mydata = {}
  if not request.user.is_authenticated:
    if request.method == 'POST':
      login_form = AuthenticationForm(request=request, data=request.POST)
      if login_form.is_valid():
        uname = login_form.cleaned_data['username']
        upass = login_form.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
          login(request, user)
          messages.success(request, "You are successfuly Signin")
          return HttpResponseRedirect("/dashboard/")
    else:
      login_form = AuthenticationForm()
    mydata = {'form': login_form}
    return render(request, "signin.html", mydata)
  else:
    return redirect("dashboard")

def editprofile(request,id):
  if request.user.is_authenticated:
    if request.method=="POST":
      if request.user.is_superuser==True:
        form=AdminUserPrifoleForm(request.POST,instance=request.user)
        form.is_valid()
        messages.success(request,"Your profile Update successfuly")
        form.save()
        return redirect('dashboard')
      else:
        form=EditUserPrifoleForm(request.POST,instance=request.user)
        form.is_valid()
        messages.success(request,"Your profile Update successfuly")
        form.save()
        return redirect('dashboard')
    else: 
      if request.user.is_superuser==True:
        form=AdminUserPrifoleForm(instance=request.user)
      else: 
        form=EditUserPrifoleForm(instance=request.user)
      data={'form':form}
      return render(request,"editprofile.html",data)
  else:
    return redirect("signin")