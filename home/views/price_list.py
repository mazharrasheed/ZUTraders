from django.shortcuts import render, redirect,get_object_or_404
from home.models import Price_List,Final_Product_Price,Price_List_Note,Price_List_Note_Products,Final_Product
from home.forms import Price_ListForm,Final_Product_PriceForm,PriceListNoteForm,PriceListNoteProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from collections import defaultdict
@login_required
@permission_required('home.add_project', login_url='/login/')
def pricelist_detail(request,id):
  print("pricelist_detail")
  price_list_note_id=None
  if request.user.is_authenticated:
    price_list=Price_List.objects.get(is_deleted=False,id=id)
    if price_list:
        data=Price_List_Note_Products.objects.filter(price_list_id=price_list.id)
        price_list_note=Price_List_Note_Products.objects.filter(price_list_id=price_list.id).first()
        if price_list_note:
        # requried for update price list not 
          price_list_note_id=price_list_note.price_list_note_id
    
    data={'mydata':data, 'price_list_note_id':price_list_note_id,
          'price_list':price_list ,'form':Final_Product_PriceForm()}
    return render(request, 'price_list/add_price_list.html', data )
  else:
    return redirect('signin')

@login_required
@permission_required('home.add_project', login_url='/login/')
def add_pricelist(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
       
        mydata=Price_List.objects.filter(is_deleted=False)
        form = Price_ListForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Region Added successfully !!")
          return redirect('pricelist')
    else:
        mydata=Price_List.objects.filter(is_deleted=False)
        
        form = Price_ListForm()
    data={'form': form, 'mydata':mydata,}
    return render(request, 'price_list/add_price_list.html', data)
  else:
    return redirect('signin')

@login_required
@permission_required('home.change_project', login_url='/login/')
def edit_pricelist(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Price_List.objects.get(id=id)
      form = Price_ListForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Region Updated successfully !!")
        return redirect('region')
    else:
      mydata=Price_List.objects.get(id=id)
      form = Price_ListForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True }
  return render(request, 'price_list/add_price_list.html', data)


from django.db.models.deletion import ProtectedError

@login_required
@permission_required('home.view_delete', login_url='/login/')
def delete_pricelist(request, id):
    try:
        mydata = get_object_or_404(Price_List, id=id)
        mydata.delete()
        messages.success(request, "Region Deleted successfully !!")
    except ProtectedError as e:
        related_objects = e.protected_objects  # Get the related objects that are blocking the delete
        messages.error(
            request, 
            f"Cannot delete '{mydata.name}' because it is referenced by: "
            f"{', '.join([str(obj) for obj in related_objects])}. Please delete the related objects first."
        )
    return redirect('pricelist')



# price List Note

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render



from django.db import IntegrityError, transaction

@login_required
@permission_required('home.add_price_list_note', login_url='/login/')
def create_price_list_note(request, id):
    # fallback: get price_list from query or from url param
    price_list_id = request.GET.get('price_list', id)
    price_list_id = int(price_list_id)
    print("Selected PriceList ID:", price_list_id)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:
            form_note = PriceListNoteForm(request.POST)
            products = request.POST.getlist('products[]')

            if form_note.is_valid() and products:
                note = form_note.save(commit=False)
                note.created_by = request.user
                note.save()
                errors = []
               
                for product_data in products:
                    try:
                        product_id, price = product_data.split(':')
                        with transaction.atomic():
                            Price_List_Note_Products.objects.create(
                                price_list_note=note,
                                price_list=note.price_list,  # ✅ from saved note
                                product_id=product_id,
                                price=price
                            )
                            
                    except IntegrityError:
                        product=Final_Product.objects.get(id=product_id)
                        errors.append(f"Product {product} already has a price in this price list.")

                if errors:
                    # Rollback the whole note if some products fail
                    note.delete()
                    return JsonResponse({
                        'success': False,
                        'errors': errors
                    }, status=400)

                return JsonResponse({'success': True, 'redirect_url': f'/price_list_detail/{price_list_id}'})

            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'}, status=400)

    # GET request → render form
    form_product = PriceListNoteProductForm()
    form_note = PriceListNoteForm(initial={'price_list': price_list_id})

    return render(request, 'price_list/create_price_list_note.html', {
        'form': form_product,
        'form_note': form_note,
        'price_list_id': price_list_id
    })



#  Edit Price in price list
@login_required
@permission_required('home.add_change_price_list_note_products', login_url='/login/')
def edit_final_product_price(request, id):
    if request.method == 'POST':
        # get raw string values
        pricelist_id = request.POST['pricelist']
        product_id = request.POST['product']
        price = request.POST['price']
        # convert to correct types
        pricelist_id = int(pricelist_id)  
        product_id = int(product_id)  
        price = float(price)  
        print(id,pricelist_id,product_id,price)
        # ✅ Update record instead of re-creating
        try:
            print("before data")
            data=Price_List_Note_Products.objects.get(id=id, price_list_id=pricelist_id, product_id=product_id)
            print(data,"fdfsdfds")
            data.price=price
            data.save()
        except:
           pass
        return redirect('pricelistdetail' , id= pricelist_id )


@login_required
@permission_required('home.add_delete_price_list_note_products', login_url='/login/')
def delete_final_product_price(request,id):
    mydata=Price_List_Note_Products.objects.get(id=id).delete()
    mydata.save()
    messages.success(request,"Product Price Deleted Successfully from List !!")
    return redirect('pricelistdetail' , id=id )

@login_required
@permission_required('home.change_price_list_note', login_url='/login/')

def edit_price_list_note(request, id):
    price_list_id=request.GET.get('price_list')
    note = get_object_or_404(Price_List_Note, pk=id)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:
            form_note = PriceListNoteForm(request.POST, instance=note)
            products = request.POST.getlist('products[]')

            note.created_by=request.user
            note.save()

            print(note.id,note.price_list)

            if note:
            #     note = form_note.save(commit=False)
            #     note.created_by = request.user
            #     note.save()

                # Clear old products and re-add new ones
                Price_List_Note_Products.objects.filter(price_list_note=note).delete()
                for product_data in products:
                    product_id, price = product_data.split(':')
                    Price_List_Note_Products.objects.create(
                        price_list_note=note,
                        price_list=note.price_list,
                        product_id=product_id,
                        price=price
                    )

                return JsonResponse({'success': True, 'redirect_url': f'/price_list_detail/{price_list_id}'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data.'})

    else:
        form_product = PriceListNoteProductForm(note=note)
        form_note = PriceListNoteForm(instance=note)

        # Existing products for pre-load in JS
        existing_products = list(
            Price_List_Note_Products.objects.filter(price_list_note=note)
            .values('id', 'product__id', 'product__productname', 'price')
        )

    return render(request, 'price_list/edit_price_list_note.html', {
        'form': form_product,
        'form_note': form_note,
        'note': note,
        'existing_products': existing_products,
        'price_list_id': price_list_id
    })