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

    product_notes=Final_Product_Note.objects.all().order_by('-id')

    data={'product_notes':product_notes}

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
