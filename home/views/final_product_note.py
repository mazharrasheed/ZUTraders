# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ..models import Final_Product_Note, Final_Product_Note_Product,Final_Product
from ..forms import FinalProductNoteForm, FinalProductNoteProductForm


@login_required
@permission_required('home.view_store_purchase_note', login_url='/login/')
def list_final_product_note(request):

    final_pro_note_pro={}

    product_notes=Final_Product_Note.objects.all().order_by('-id')

    for x in product_notes:
        final_pro_note_pro[x.id]=Final_Product_Note_Product.objects.filter(final_product_note=x).count()


    data={'product_notes':product_notes,'final_pro_note_pro':final_pro_note_pro}

    return render(request, 'final_product_note/list_final_pro_note.html',data)


@login_required
@permission_required('home.add_final_product_note', login_url='/login/')
def create_final_product_note(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if "finalize" in request.POST:
            form_note = FinalProductNoteForm(request.POST)

            products = request.POST.getlist("products[]")
            if form_note.is_valid() and products:
                note = form_note.save(commit=False)
                note.created_by = request.user
                note.save()

                for product_data in products:
                    product_id, quantity = product_data.split(":")
                    pro=Final_Product_Note_Product.objects.create(
                        final_product_note=note,
                        product_id=product_id,
                        quantity=quantity,
                    )

                    Final_Product.objects.get(id=product_id).change_status()



                return JsonResponse({"success": True, "redirect_url": "/list-final-pro-note/"})
            else:
                return JsonResponse({"success": False, "errors": "Invalid data or no products."})

    else:
        form_note = FinalProductNoteForm()
        form_product = FinalProductNoteProductForm()

    return render(request, "final_product_note/create_final_note.html", {
        "form_note": form_note,
        "form_product": form_product,
    })


@login_required
@permission_required('home.change_final_product_note', login_url='/login/')
def edit_final_product_note(request, id):
    note = get_object_or_404(Final_Product_Note, pk=id)
    existing_products_qs = Final_Product_Note_Product.objects.filter(final_product_note=note).select_related('product')

    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        form_note = FinalProductNoteForm(request.POST, instance=note)

        products = request.POST.getlist("products[]")             # list of "productId:quantity"
        deleted_products = request.POST.getlist("deleted_products[]")  # list of product ids to delete

        if form_note.is_valid():
            note = form_note.save(commit=False)
            note.updated_by = request.user
            note.save()

            # Delete removed products (if any)
            if deleted_products:
                Final_Product_Note_Product.objects.filter(
                    final_product_note=note, product_id__in=deleted_products
                ).delete()

            # Add/update remaining products
            # We will update_or_create by (final_product_note, product_id)
            for product_data in products:
                try:
                    product_id, quantity = product_data.split(":")
                except ValueError:
                    continue
                obj, created = Final_Product_Note_Product.objects.update_or_create(
                    final_product_note=note,
                    product_id=product_id,
                    defaults={'quantity': quantity},
                )
                # update product status (same as create logic)
                try:
                    Final_Product.objects.get(id=product_id).change_status()
                except Final_Product.DoesNotExist:
                    pass

            return JsonResponse({"success": True, "redirect_url": "/list-final-pro-note/"})
        else:
            return JsonResponse({"success": False, "errors": form_note.errors})

    else:
        # GET: render form with instance and the existing products
        form_note = FinalProductNoteForm(instance=note)
        form_product = FinalProductNoteProductForm()
        existing_products = list(existing_products_qs)  # pass to template

    return render(request, "final_product_note/edit_final_note.html", {
        "form_note": form_note,
        "form_product": form_product,
        "existing_products": existing_products,
        "note": note,
    })


from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

@login_required
@permission_required('home.delete_final_product_note', login_url='/login/')
def delete_final_product_note(request, id):
    """
    Deletes a Final Product Note and all its related products.
    Works for both AJAX and normal form submissions.
    """
    note = get_object_or_404(Final_Product_Note, id=id)
    if request.method == "POST":
        # Delete related products first
        Final_Product_Note_Product.objects.filter(final_product_note=note).delete()
        # Then delete the note itself
        note.delete()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect_url": "/list-final-pro-note/"})
        else:
            return redirect("list_final_product_note")

    # If GET → ask for confirmation
    return JsonResponse({"success": False, "message": "Invalid request method"})

@login_required
@permission_required('home.view_sales_receipt', login_url='/login/')
def print_final_product_note(request, id):
    # Fetch the salereceipt instance by ID
    pronote = get_object_or_404(Final_Product_Note, id=id)
    # Fetch all products associated with this salereceipt
    pronote_products = Final_Product_Note_Product.objects.filter(final_product_note=pronote)
   
    return render(request, 'final_product_note/print_final_note.html', {
        'pronote': pronote,
        'pronote_products': pronote_products,

    })