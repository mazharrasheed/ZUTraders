from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit
from django import forms
from django.forms import DateTimeInput
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import User,Group
from django.utils.translation import gettext_lazy as _

from .models import Blog
# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Category,Product,Account,Transaction,GatePassProduct,GatePass,Unit,Sales_Receipt,Inventory
from .models import Customer,Sales_Receipt_Product,Suppliers,Cheque,Employee,Product_Price,Project,Final_Product
from .models import Store_Issue_Note,Store_Issue_Product,Store_Purchase_Note,Store_Purchase_Product,Finish_Product_Category
from .models import Store_Issue_Request,Store_Issue_Request_Product,Region,Final_Product_Price,Company,Final_Product_Note,Final_Product_Note_Product,Price_List,Price_List_Note,Price_List_Note_Products


class Create_User_Form(UserCreationForm):
    username=UsernameField()
    group=forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select Group")
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Fieldset(
                'Create User',
            ),
            Field('username','group','password1','password2', css_class="mb-3", css_id="custom_field_id",),
            Submit('submit', 'Create User', css_class='btn btn-info mt-3'),
        )


class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = ['name']

class Price_ListForm(forms.ModelForm):

    class Meta:
        model = Price_List
        fields = ['name']

class CopanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name']

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

class Finish_Product_CategoryForm(forms.ModelForm):

    class Meta:
        model = Finish_Product_Category
        fields = ['name']

# class Finished_product_Form(forms.ModelForm):

#     class Meta:
#         model = Finish_Product
#         fields = ['name','size','weight']
#         labels={'name':'Product Name','size':'Sizes','weight':'Weight in Kgs',}

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

class Finish_ProductForm(forms.ModelForm):
    # unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select Unit")
    category = forms.ModelChoiceField(queryset=Finish_Product_Category.objects.filter(is_deleted=False), empty_label="Select Category")
    class Meta:
        model = Final_Product
        fields = ['productname','category',]
        labels={'productname':'Product Name',
                }

        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),

        }

    def __init__(self, *args, **kwargs):
        super(Finish_ProductForm, self).__init__(*args, **kwargs)


        placeholders = {
            'productname': 'Enter product name',
            'category':'Select Category',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Add 'fs-5' class to all fields' labels
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'

        # self.fields['category'].empty_label = "Select Category"
    


class ProductForm(forms.ModelForm):
    # unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select Unit")
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_deleted=False), empty_label="Select Category")
    class Meta:
        model = Product
        fields = [ 'productname','unit','category','final_product_group','default_store','stockable','rate','labour','weight','stock']
        labels={'productname':'Product Name',
                'product_status':'Product_Status'}

        widgets = {

            'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            "stockable": forms.Select(
                choices=[(True, "Yes"), (False, "No")],
                attrs={"class": "form-select"}
            ),

        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


        placeholders = {
            'productname': 'Enter product name',
            'unit':'Select Unit',
            'weight':'Enter product weight',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Add 'fs-5' class to all fields' labels
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'

        self.fields['category'].empty_label = "Select"
        self.fields['final_product_group'].empty_label = "Select"
        self.fields['default_store'].choices = [('', 'Select')] + list(self.fields['default_store'].choices)

class Product_PriceForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")

    class Meta:
        model = Product_Price
        fields = ['product', 'customer', 'price']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)  # Get the category from kwargs
        super(Product_PriceForm, self).__init__(*args, **kwargs)

        # Filter products based on the selected category
        if category:
            self.fields['product'].queryset = Product.objects.filter(category=category, is_deleted=False)

        placeholders = {
            'price': 'Enter product price here',
        }

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})



class Final_Product_PriceForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Final_Product.objects.filter(is_deleted=False),
        empty_label="Select Product"
    )
    price_list = forms.ModelChoiceField(
        queryset=Price_List.objects.filter(is_deleted=False),
        empty_label="Select Price List",
        required=True
    )

    class Meta:
        model = Final_Product_Price
        fields = ['product', 'price_list', 'price']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super(Final_Product_PriceForm, self).__init__(*args, **kwargs)
        self.fields['price_list'].label="Price List"
        # Filter products by category if provided
        print('category from forms',category)
        if category:
            self.fields['product'].queryset = Final_Product.objects.filter(
                category_id=category.id if hasattr(category, "id") else category,
                is_deleted=False
            )
        placeholders = {
            'price': 'Enter final product price',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        price_list = cleaned_data.get("price_list")
        # Rule 1: At least one must be provided
        if not price_list :
            raise forms.ValidationError("Price list must be selected.")
        # Rule 2: Prevent duplicate for same product + customer
        if price_list and Final_Product_Price.objects.filter(
            product=product, price_list=price_list, is_deleted=False
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f"A price already exists for product '{product}' and price_list '{price_list}'."
            )
        return cleaned_data
    

# price list note 

# class PriceListNoteForm(forms.ModelForm):
#     price_list = forms.ModelChoiceField(
#         queryset=Price_List.objects.filter(is_deleted=False),
#         empty_label="Select Price List"
#     )

#     class Meta:
#         model = Price_List_Note
#         fields = []

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             first_price_list = self.instance.price_list.first()
#             if first_price_list:
#                 self.fields['price_list'].initial = first_price_list

#         # Add 'fs-5' class to all fields' labels
#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
#             self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'


# class PriceListNoteProductForm(forms.ModelForm):
#     product = forms.ModelChoiceField(
#         queryset=Final_Product.objects.filter(is_deleted=False),
#         empty_label="Select Product"
#     )
#     price = forms.FloatField(min_value=0, label="Price")

#     class Meta:
#         model = Price_List_Note_Products
#         fields = ['product', 'price']

#     def __init__(self, *args, **kwargs):
#         self.note = kwargs.pop('note', None)
#         super().__init__(*args, **kwargs)

#         print(kwargs)

#         placeholders = {
#             'price': 'Enter Price',
#         }
#         for field_name, placeholder in placeholders.items():
#             self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

#         # Add 'fs-5' class to all fields' labels
#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
#             self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'

#     def clean(self):
#         cleaned_data = super().clean()
#         product = cleaned_data.get('product')
#         if product and self.note:
#             if Price_List_Note_Products.objects.filter(price_list_note=self.note, product=product).exists():
#                 self.add_error('product', f'The product "{product}" has already been added to this note.')
#         return cleaned_data

class PriceListNoteForm(forms.ModelForm):
    price_list = forms.ModelChoiceField(
        queryset=Price_List.objects.filter(is_deleted=False),
        empty_label="Select Price List"
    )

    class Meta:
        model = Price_List_Note
        fields = ['price_list']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['price_list'].initial = self.instance.price_list

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'


class PriceListNoteProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Final_Product.objects.filter(is_deleted=False),
        empty_label="Select Product"
    )
    price = forms.FloatField(min_value=0, label="Price")

    class Meta:
        model = Price_List_Note_Products
        fields = ['product', 'price']

    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        super().__init__(*args, **kwargs)

        placeholders = {'price': 'Enter Price'}
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.note:
            if Price_List_Note_Products.objects.filter(price_list_note=self.note, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this note.')
        return cleaned_data


class search_Product_PriceForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)  # Get the category from kwargs
        super(search_Product_PriceForm, self).__init__(*args, **kwargs)

        # Filter products based on the selected category
        if category:
            self.fields['product'].queryset = Product.objects.filter(category=category, is_deleted=False)

class GatePassForm(forms.ModelForm):

    RETURNABLE_CHOICES = (
        (True, 'Returnable'),
        (False, 'Non-returnable'),
    )

    returnable = forms.ChoiceField(choices=RETURNABLE_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = GatePass
        fields = ['returnable','vehicle', 'driver_phone_number','dispatch_for', 'name_of_site', 'person_name', 'phone_number']


class GatePassProductForm(forms.ModelForm):

    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    remarks = forms.CharField( label='Remarks',required=False)

    class Meta:
        model = GatePassProduct
        fields = ['product', 'quantity','remarks']

    def __init__(self, *args, **kwargs):
        self.gatepass = kwargs.pop('gatepass', None)
        super(GatePassProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        if product and self.gatepass:
            if GatePassProduct.objects.filter(gatepass=self.gatepass, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')

        return cleaned_data


class Store_Issue_Request_Form(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_deleted=False),
        empty_label="Select Project"
    )
    class Meta:
        model = Store_Issue_Request
        fields = ['project']
    def __init__(self, *args, **kwargs):
        super(Store_Issue_Request_Form, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['project'].initial = self.instance.project

class Store_Issue_Request_ProductForm(forms.ModelForm):

    # product = forms.ModelChoiceField(queryset=Product.objects.filter(inventory__quantity__gt=0).distinct(), empty_label="Select Product")
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False,product_status=True), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    # unit_price = forms.FloatField( label='Unit Price',required=False)

    class Meta:
        model = Store_Issue_Request_Product
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Store_Issue_Request_ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Store_Issue_Request_Product.objects.filter(store_issue_request=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')
        return cleaned_data


class Store_issue_Form(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_deleted=False),
        empty_label="Select Project"
    )
    class Meta:
        model = Store_Issue_Note
        fields = ['project']
    def __init__(self, *args, **kwargs):
        super(Store_issue_Form, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['project'].initial = self.instance.project



class Store_Issue_ProductForm(forms.ModelForm):

    # product = forms.ModelChoiceField(queryset=Product.objects.filter(inventory__quantity__gt=0).distinct(), empty_label="Select Product")
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False,product_status=True), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    # unit_price = forms.FloatField( label='Unit Price',required=False)

    class Meta:
        model = Store_Issue_Product
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Store_Issue_ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Store_Issue_Product.objects.filter(store_issue_request=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')
        return cleaned_data

class FinalProductNoteForm(forms.ModelForm):
    class Meta:
        model = Final_Product_Note
        fields = []  # date_created + created_by handled in view


class FinalProductNoteProductForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Final_Product.objects.filter(is_deleted=False,),
        empty_label="Select Product"
    )

    class Meta:
        model = Final_Product_Note_Product
        fields = ['product', 'quantity']
        widgets = {
            'remarks': forms.TextInput(attrs={'placeholder': 'Optional remarks'})
        }

class Store_Purchase_Form(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_deleted=False),
        empty_label="Select Project",required=False
    )
    class Meta:
        model = Store_Purchase_Note
        fields = ['project']
    def __init__(self, *args, **kwargs):
        super(Store_Purchase_Form, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['project'].initial = self.instance.project



class Store_Purchase_ProductForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_deleted=False),
        empty_label="Select Product",
        required=False
    )

    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    # unit_price = forms.FloatField( label='Unit Price',required=False)

    class Meta:
        model = Store_Purchase_Product
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Store_Purchase_ProductForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Store_Purchase_Product.objects.filter(store_purchase_note=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this Purchase note.')
        return cleaned_data

class Sales_ReceiptForm(forms.ModelForm):
    customer_name = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_deleted=False),
        empty_label="Select Customer",
        required=False
    )

    class Meta:
        model = Sales_Receipt
        fields = ['customer_name',]

    def __init__(self, *args, **kwargs):
        super(Sales_ReceiptForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['customer_name'].initial = self.instance.customer_name
            
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer_name")
        region = cleaned_data.get("region")

        if not customer and not region:
            raise forms.ValidationError("Either Customer or Region must be selected.")

        return cleaned_data

from django.db.models import Exists, OuterRef

class Sales_Receipt_ProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Final_Product.objects.filter(
            is_deleted=False,
            product_status=True
        ),
        empty_label="Select Product"
    )
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity")

    class Meta:
        model = Sales_Receipt_Product
        fields = ['product', 'quantity']

# class Sales_ReceiptForm(forms.ModelForm):
#     customer_name = forms.ModelChoiceField(
#         queryset=Customer.objects.filter(is_deleted=False),
#         empty_label="Select Customer",required=True
#     )
#     Region = forms.ModelChoiceField(
#         queryset=Region.objects.filter(is_deleted=False),
#         empty_label="Select Region",required=True
#     )
#     class Meta:
#         model = Sales_Receipt
#         fields = ['customer_name','region']
#     def __init__(self, *args, **kwargs):
#         super(Sales_ReceiptForm, self).__init__(*args, **kwargs)
#         # Check if an instance is passed
#         if self.instance and self.instance.pk:
#             # Set the initial value of customer_name
#             self.fields['customer_name'].initial = self.instance.customer_name
#             self.fields['region'].initial = self.instance.region


# class Sales_Receipt_ProductForm(forms.ModelForm):
#     product = forms.ModelChoiceField(queryset=Final_Product.objects.filter(is_deleted=False), empty_label="Select Product")
#     quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
#     # unit_price = forms.FloatField( label='Unit Price',required=False)

#     class Meta:
#         model = Sales_Receipt_Product
#         fields = ['product', 'quantity']

#     def __init__(self, *args, **kwargs):
#         self.salereceipt = kwargs.pop('salereceipt', None)
#         super(Sales_Receipt_ProductForm, self).__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super().clean()
#         product = cleaned_data.get('product')
#         if product and self.salereceipt:
#             if Sales_Receipt_Product.objects.filter(salereceipt=self.salereceipt, product=product).exists():
#                 self.add_error('product', f'The product "{product}" has already been added to this Sales Reciept.')
#         return cleaned_data

class Sales_Cash_ReceiptForm(forms.ModelForm):
    customer=forms.CharField(max_length=220 , required=True)
    phone_number=forms.CharField(max_length=12 , required=True)
    class Meta:
        model = Sales_Receipt
        fields = ['customer', 'phone_number']
    def __init__(self, *args, **kwargs):
        super(Sales_Cash_ReceiptForm, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['customer'].initial = self.instance.customer

class Sales_Cash_Receipt_ProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False,product_status=True), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    unit_price = forms.FloatField( label='Unit Price',required=True)

    class Meta:
        model = Sales_Receipt_Product
        fields = ['product', 'quantity','unit_price']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Sales_Cash_Receipt_ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Sales_Receipt_Product.objects.filter(salereceipt=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')
        return cleaned_data


class Sign_Up(UserCreationForm):

    username=UsernameField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Fieldset(
                'Sign Up',
            ),
            Field('username','password1','password2', css_class="mb-3", css_id="custom_field_id",),

            Submit('submit', 'SignUp', css_class='btn btn-info mt-3'),
        )

class Add_Blog(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title','description')

class EditUserPrifoleForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]
        labels={'email':'Email'}

class AdminUserPrifoleForm(UserChangeForm):

    password=None
    class Meta:
        model=User
        fields='__all__'
        labels={'email':'Email'}


class Employee_form(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [ 'name','fname','cnic','designation','address','salary','instalment','type','order','contact']
        labels={'name':'Name', 'fname':'S/o','cnic':'CNIC #',
                'contact':'Mobile'}

        widgets = {


        }

    def __init__(self, *args, **kwargs):
        super(Employee_form, self).__init__(*args, **kwargs)
        if self.fields['type'].choices:
            # remove any default ('', '---------') before prepending "Select"
            cleaned_choices = [(val, label) for val, label in self.fields['type'].choices if val != '']
            self.fields['type'].choices = [('', 'Select')] + cleaned_choices
            self.fields['order'].required=False

        if self.fields['designation'].choices:
            # remove any default ('', '---------') before prepending "Select"
            cleaned_choices = [(val, label) for val, label in self.fields['designation'].choices if val != '']
            self.fields['designation'].choices = [('', 'Select')] + cleaned_choices

        placeholders = {

            'name': 'Enter full name',
            'fname': 'Enter full father name',
            'cnic': 'xxxxxxxxxxxxx',
            'contact': 'xxxx-xxxxxxx',
            'address':'Enter Adress here',
            'designation':'Enter designation here',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Add 'fs-5' class to all fields' labels
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'


class Suppliers_form(forms.ModelForm):

    class Meta:
        model = Suppliers
        fields = ['coname', 'name','contact','adress','description']
        labels={'coname':'Company Name','name':'Name',
                'contact':'Contact','adress':'Adress','description':'Description',}

        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(Suppliers_form, self).__init__(*args, **kwargs)
        placeholders = {
            'coname': 'Enter company name',
            'name': 'Enter full name',
            'contact': '0000-0000000',
            'adress':'Enter Adress here'
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

class Customer_form(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['coname', 'name','region','contact','address','city','contact','mobile','credit_limit','price_list']
        labels={'coname':'Company Name','name':'Name',
                'contact':'Contact','address':'Address',}
    def __init__(self, *args, **kwargs):
        super(Customer_form, self).__init__(*args, **kwargs)
        self.fields['region'].empty_label = "Select Region"
        self.fields['price_list'].empty_label = "Select Price List"
        placeholders = {
            'coname': 'Enter business name',
            'name': 'Enter contact person full name',
            'region':'Select Region',
            'contact': 'xxxx-xxxxxxx',
            'address':'Enter Address here'
        }

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Add 'fs-5' class to all fields' labels
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'

class Cheques_form(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")
    class Meta:
        model = Cheque
        fields = ['customer', 'cheque_number','cheque_amount','cheque_date','bank_name']
        labels={'customer':'Customer Name','cheuqe_Number':'Cheque Number','cheque_date':'Cheque Date','bank_name':'Bank Name/Party Name'
            }
        widgets = {
            'cheque_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(Cheques_form, self).__init__(*args, **kwargs)
        self.fields['cheque_number'].required = False
        self.fields['bank_name'].required = False
        placeholders = {
            'cheque_number': 'Enter cheque number',
            'bank_name':'Enter bank name',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})




class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name','account_type','address','contact','mobile']
        labels={'contact':'Contact #','mobile':'Mobile #'}

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['name'].required = True
        choices = list(self.fields['account_type'].choices)
        # Remove the empty one if it exists
        choices = [(k, v) for k, v in choices if k != '']
        self.fields['account_type'].choices = [('', 'Select')] + choices

class Employee_AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['employee','account_type']

    def __init__(self, *args, **kwargs):
        super(Employee_AccountForm, self).__init__(*args, **kwargs)

        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)

        self.fields['employee'].empty_label = "Select"
        self.fields['employee'].required = True
        choices = list(self.fields['account_type'].choices)
        # Remove the empty one if it exists
        choices = [(k, v) for k, v in choices if k != '']
        self.fields['account_type'].choices = [('', 'Select')] + choices

class Customer_AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['customer','account_type']

    def __init__(self, *args, **kwargs):
        super(Customer_AccountForm, self).__init__(*args, **kwargs)

        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['customer'].empty_label = "Select"
        self.fields['customer'].required = True
        choices = list(self.fields['account_type'].choices)
        # Remove the empty one if it exists
        choices = [(k, v) for k, v in choices if k != '']

        self.fields['account_type'].choices = [('', 'Select')] + choices

class Supplier_AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['supplier','account_type']

    def __init__(self, *args, **kwargs):
        super(Supplier_AccountForm, self).__init__(*args, **kwargs)

        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['supplier'].empty_label = "Select"
        self.fields['supplier'].required = True
        choices = list(self.fields['account_type'].choices)
        # Remove the empty one if it exists
        choices = [(k, v) for k, v in choices if k != '']

        self.fields['account_type'].choices = [('', 'Select')] + choices



class Cheque_AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['cheque','balance','account_type']

    def __init__(self, *args, **kwargs):
        super(Cheque_AccountForm, self).__init__(*args, **kwargs)

        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['cheque'].empty_label = "Select"
        self.fields['cheque'].required = True
        choices = list(self.fields['account_type'].choices)
        # Remove the empty one if it exists
        choices = [(k, v) for k, v in choices if k != '']

        self.fields['account_type'].choices = [('', 'Select')] + choices


class TransactionForm(forms.ModelForm):

    
    class Meta:
        model = Transaction
        fields = ['description', 'debit_account','credit_account','amount','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['debit_account'].empty_label = "Select"
        self.fields['credit_account'].empty_label = "Select"
        self.fields['debit_account'].queryset = Account.objects.filter(is_deleted=False)
        self.fields['credit_account'].queryset = Account.objects.filter(is_deleted=False)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount



class AccountStatementForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label="Account",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Account"
    )
    from_date = forms.DateField(
        required=True,
        label="From Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    to_date = forms.DateField(
        required=True,
        label="To Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )