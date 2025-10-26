
from django.shortcuts import render, redirect,get_object_or_404
from home.models import Company
from home.forms import CopanyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.add_project', login_url='/login/')
def add_company(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
       
        mydata=Company.objects.filter(is_deleted=False)
        form = CopanyForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Company Added successfully !!")
          return redirect('company')
    else:
        mydata=Company.objects.filter(is_deleted=False)
        
        form = CopanyForm()
    data={'form': form, 'mydata':mydata,}
    return render(request, 'company/add_company.html', data)
  else:
    return redirect('signin')
@login_required
@permission_required('home.change_project', login_url='/login/')
def edit_company(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Company.objects.get(id=id)
      form = CopanyForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Company Updated successfully !!")
        return redirect('company')
    else:
      mydata=Company.objects.get(id=id)
      form = CopanyForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True }
  return render(request, 'company/add_company.html', data)


# @login_required
# @permission_required('home.view_delete', login_url='/login/')

# def delete_project(request,id):
 
#     mydata=Company.objects.get(id=id)
#     mydata.is_deleted=True
#     mydata.save()
#     messages.success(request,"Company Deleted successfully !!")
#     return redirect('company')

from django.db.models.deletion import ProtectedError

@login_required
@permission_required('home.view_delete', login_url='/login/')
def delete_company(request, id):
    try:
        mydata = get_object_or_404(Company, id=id)
        mydata.delete()
        messages.success(request, "Company Deleted successfully !!")
    except ProtectedError as e:
        related_objects = e.protected_objects  # Get the related objects that are blocking the delete
        messages.error(
            request, 
            f"Cannot delete '{mydata.name}' because it is referenced by: "
            f"{', '.join([str(obj) for obj in related_objects])}. Please delete the related objects first."
        )
    return redirect('company')