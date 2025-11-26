from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import Add_Blog, AdminUserPrifoleForm, EditUserPrifoleForm, GatePassProductForm,Sign_Up
from ..models import Blog,GatePass, GatePassProduct,Employee,Customer,Suppliers,Account,Product,Final_Product,Sales_Receipt,Sales_Receipt_Product,Transaction
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import json
# Create your views here.

@login_required

def index(request):
    users=User.objects.all().count()
    customers=Customer.objects.all().count()
    suppliers=Suppliers.objects.all().count()
    employees=Employee.objects.all().count()
    accounts=Account.objects.all().count()
    items=Product.objects.all().count()
    sales=Sales_Receipt.objects.all().count()

    for account in Account.objects.all():
        print(account.customer == None)
        if account.customer != None :
            initial_transaction=Transaction.objects.filter(description="Initial transaction opening balance",transaction_type='Sales').aggregate(total=Sum('amount'))['total'] or 0
            print(initial_transaction)
    salereceipts = Sales_Receipt.objects.all()
    monthly_sales = {}
    salereceipt_items_pro = {}
    total_amount = {}

    # ✅ Monthly totals using TruncMonth
    monthly_data = (
        Sales_Receipt_Product.objects
        .values('salereceipt__date_created')  # assuming Sales_Receipt has a 'date' field
        .annotate(month=TruncMonth('salereceipt__date_created'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Per receipt totals
    for x in salereceipts:
        salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
        total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))

    total_sale = sum(item['amount__sum'] or 0 for item in total_amount.values())


    # Convert to dict with month names
    for entry in monthly_data:
        month_name = DateFormat(entry['month']).format('M-Y')  # e.g. Jan, Feb
        monthly_sales[month_name] = entry['total']
        labels = list(monthly_sales.keys())
        values = list(monthly_sales.values())

    # print(monthly_sales,labels,values)


    # Check if the user has the required permission
    if not request.user.has_perm('home.view_dashboard'):
        # Custom redirect logic for users without permission
        if request.user.is_superuser:
            return redirect('/')
        elif request.user.groups.filter(name='checker').exists():
            return redirect('/')
        elif request.user.groups.filter(name='author').exists():
            return redirect('/dashboard/')
        elif request.user.groups.filter(name='accountant').exists():
            return redirect('/accounts/')
        elif request.user.groups.filter(name='storekeeper').exists():
            return redirect('/store/')
        elif request.user.groups.filter(name='salesman').exists():
            return redirect('/list-sales/')
        elif request.user.groups.filter(name="incharge").exists():
            return redirect("/list-store-issue-request/")
        else:
            raise PermissionDenied  # Show 403 Forbidden page

    chart_data = {
        "labels": labels,
        "values": values
    }

    data={'users':users,
          'employees':employees,
          'customers':customers,
          'suppliers':suppliers,
          'accounts':accounts,
          'items':items,
          'sales':sales,
          'total_sale':float(total_sale)+float(initial_transaction),
          "chart_data_json": json.dumps(chart_data)}
    return render(request, 'index.html',data)

@login_required
def detail(request,id):
  myblog=Blog.objects.get(id=id)
  data={'myblog':myblog}
  return render(request,'detail.html',data)

@login_required
@permission_required('home.change_blog',login_url='/login/')
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


@login_required
@permission_required('home.delete_blog',login_url='/login/')
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

@login_required
@permission_required('home.add_blog',login_url='/login/')
def post_blog(request):
  
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
  
@login_required
@permission_required('home.view_blog',login_url='/login/')
def dashboard(request):
  
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
      return redirect('signin')
  else:
    form=Sign_Up()
  data={'form':form}
  return render(request,'auth-sign-up.html',data)
  # return render(request,'signup.html',data)

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
          messages.success(request, "You are Successfuly Signin")

          # if user.is_superuser:
          #   return HttpResponseRedirect("/")
          # elif user.groups == "author":
          #   return HttpResponseRedirect("/dashboard/")
          # elif user.groups == "accountant":
          #   return HttpResponseRedirect("/accounts/")
          # elif user.groups=="storekeeper":
          #   return HttpResponseRedirect("/store/")
          # elif user.groups=="salesman":
          #   return HttpResponseRedirect("/list-sales/")
          if user.is_superuser:
              return redirect("/")
          elif user.groups.filter(name="author").exists():
            return redirect("/dashboard/")
          elif user.groups.filter(name="accountant").exists():
            return redirect("/accounts/")
          elif user.groups.filter(name="storekeeper").exists():
            return redirect("/store/")
          elif user.groups.filter(name="incharge").exists():
            return redirect("/list-store-issue-request/")
          elif user.groups.filter(name="salesman").exists():
            return redirect("/list-sales/")
    else:
      login_form = AuthenticationForm()
    mydata = {'form': login_form}
    return render(request, "auth-normal-sign-in.html", mydata)
  else:
    return redirect("index")

@login_required
# @permission_required('auth.change_user',login_url='/login/')
def editprofile(request,id):
 
  if request.method=="POST":
    if request.user.is_superuser==True:
      form=AdminUserPrifoleForm(request.POST,instance=request.user)
      form.is_valid()
      messages.success(request,"Your profile Update successfully")
      form.save()
      return redirect('dashboard')
    else:
      form=EditUserPrifoleForm(request.POST,instance=request.user)
      form.is_valid()
      messages.success(request,"Your Profile Update Successfully")
      form.save()
      return redirect('dashboard')
  else: 
    if request.user.is_superuser==True:
      form=AdminUserPrifoleForm(instance=request.user)
    else: 
      form=EditUserPrifoleForm(instance=request.user)
    data={'form':form}
    return render(request,"editprofile.html",data)





