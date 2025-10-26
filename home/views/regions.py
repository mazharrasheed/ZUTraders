from django.shortcuts import render, redirect,get_object_or_404
from home.models import Region
from home.forms import RegionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required

@login_required
@permission_required('home.add_project', login_url='/login/')
def add_Region(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
       
        mydata=Region.objects.filter(is_deleted=False)
        form = RegionForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Region Added successfully !!")
          return redirect('region')
    else:
        mydata=Region.objects.filter(is_deleted=False)
        
        form = RegionForm()
    data={'form': form, 'mydata':mydata,}
    return render(request, 'regions/add_region.html', data)
  else:
    return redirect('signin')

@login_required
@permission_required('home.change_project', login_url='/login/')
def edit_region(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Region.objects.get(id=id)
      form = RegionForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Region Updated successfully !!")
        return redirect('region')
    else:
      mydata=Region.objects.get(id=id)
      form = RegionForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True }
  return render(request, 'regions/add_region.html', data)


from django.db.models.deletion import ProtectedError

@login_required
@permission_required('home.view_delete', login_url='/login/')
def delete_region(request, id):
    try:
        mydata = get_object_or_404(Region, id=id)
        mydata.delete()
        messages.success(request, "Region Deleted successfully !!")
    except ProtectedError as e:
        related_objects = e.protected_objects  # Get the related objects that are blocking the delete
        messages.error(
            request, 
            f"Cannot delete '{mydata.name}' because it is referenced by: "
            f"{', '.join([str(obj) for obj in related_objects])}. Please delete the related objects first."
        )
    return redirect('region')