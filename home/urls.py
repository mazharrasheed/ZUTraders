from django.contrib import admin
from django.urls import  path
from home.views import category,product
from home.views import users,views,accounts,store_issue,store_purchase,finished_product,finished_pro_category
from home.views import gatepass,sales,suppliers,customers,cheques,employees,prices,company,store_issue_request
from home.views import regions,final_product_note,price_list
from django.conf.urls.static import static

from Inventry_management_System import settings


urlpatterns = [
    
# Auth and Blog
    path('', views.index,name="index"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('postblog/', views.post_blog,name="postblog"),
    path('signup/', views.sign_up,name="signup"),
    path('signin/', views.sign_in,name="signin"),
    path('login/', views.sign_in,name="signin"),
    path('logout/', views.log_out,name="logout"),

# Users
    path('list_users/', users.list_users,name="listusers"),
    path('create_user/', users.create_user,name="createuser"),
    path('user_detail/<int:id>', users.user_details,name="userdetail"),
# path('accounts/login/', views.sign_in,name="signin"),@login requried hit this url
    path('detail/<int:id>', views.detail,name="detail"),
    path('delete/<int:id>', views.delete_data , name="deletedata"),
    path('edit/<int:id>', views.edit_data , name="editdata"),
    path('editprofile/<int:id>', views.editprofile , name="editprofile"),

# Companies
    path('company/', company.add_company , name="company"),
    path('company/<int:id>', company.edit_company , name="editcompany"),
    path('deleteproject/<int:id>', company.delete_company , name="deletecompany"),

# Regions
    path('region/', regions.add_Region , name="region"),
    path('region/<int:id>', regions.edit_region , name="editregion"),
    path('deleteregion/<int:id>',regions.delete_region , name="deleteregion"),

# Price List
    path('prices_list/', price_list.add_pricelist , name="pricelist"),
    path('price_list_detail/<int:id>', price_list.pricelist_detail , name="pricelistdetail"),
    path('addd_price_list/<int:id>', price_list.edit_pricelist , name="editpricelist"),
    path('delete_price_list/<int:id>',price_list.delete_pricelist , name="deletepricelist"),

# Price List Note

    path('create-price-list-note/', price_list.create_price_list_note, name='create_price_list_note'),
    path('create-price-list-note/<int:id>', price_list.create_price_list_note, name='create_price_list_note'),
    path('edit-price-list-note/<int:id>', price_list.edit_price_list_note, name='edit_price_list_note'),
    path('edit_final_product_price/<int:id>', price_list.edit_final_product_price, name="editfinalproductprice"),

# Product Category
    path('category/', category.add_category , name="category"),
    path('category/<int:id>', category.edit_category , name="editcategory"),
    path('deletecategory/<int:id>', category.delete_category , name="deletecategory"),

# Finshed Category
    path('finished-product-category/', finished_pro_category.add_category , name="finished_product_category"),
    path('finished-product-category/<int:id>', finished_pro_category.edit_category , name="edit_finished_product_category"),
    path('finished-product-deletecategory/<int:id>', finished_pro_category.delete_category , name="delete_finished_product_category"),

# Products
    path('store/', product.store , name="store"),
    path('product/', product.products , name="product"),
    path('add_product/<int:id>', product.add_product , name="addproduct1"),
    path('add_product/', product.add_product , name="addproduct"),
    path('add_product1/', product.add_product1 , name="addproduct2"),
    path('product/<int:id>', product.edit_product , name="editproduct"),
    path('deleteproduct/<int:id>', product.delete_product , name="deleteproduct"),
    path('inventory/', product.inventory , name="store_inventory"),

# Finished Products
    path('finished_product/', finished_product.products , name="finishedproduct"),
    path('add-finished-product/<int:id>', finished_product.add_product , name="addfinishedproduct1"),
    path('add-finished-product/', finished_product.add_product , name="addfinishedproduct"),
    path('add-finished-productmain/', finished_product.add_productmain , name="addfinishedproductmain"),
    path('edit-finished-product/<int:id>', finished_product.edit_product , name="editfinishedproduct"),
    path('delete-finished-product/<int:id>', finished_product.delete_product , name="deletefinishedproduct"),
    path('delete-finished-product1/<int:id>', finished_product.delete_product1 , name="deletefinishedproduct1"),

# Search Product and Product Price
    path('search_product_price/<int:id>', prices.search_product_price , name="searchproductprice"),
    path('add_product_price/<int:id>', prices.add_product_price , name="addproductprice"),
    path('edit_product_price/<int:id>', prices.edit_product_price , name="editproductprice"),
    path('deleteproduct_price/<int:id>', prices.delete_product_price , name="deleteproductprice"),

# Search Product and Final Product Price
    path('list_product_price/', prices.list_product_prices , name="listproductprices"),
    path('search_product_price/<int:id>', prices.search_product_price , name="searchproductprice"),
    path('add_final_product_price/<int:id>', prices.add_final_product_price , name="addfinalproductprice"),
    path('add_final_product_pricemain/', prices.add_final_product_pricemain , name="addfinalproductpricemain"),
    path('edit_final_product_pricemain/<int:id>', prices.edit_final_product_pricemain , name="editfinalproductpricemain"),
    path('edit_final_product_price/<int:id>', prices.edit_final_product_price , name="editfinalproductprice"),
    path('deleteproduct_price/<int:id>', prices.delete_final_product_price , name="deletefinalproductprice"),

# Employees
    path('employees/', employees.employees , name="employees"),
    path('employees_detail/<int:id>', employees.employees_detail , name="employeesdetail"),
    path('add_employee/', employees.add_employee , name="addemployee"),
    path('editemployee/<int:id>', employees.edit_employee , name="editemployee"),
    path('deleteemployee/<int:id>', employees.delete_employee , name="deleteemployee"),

# Suppliers
    path('suppliers/', suppliers.supplier , name="suppliers"),
    path('add_supplier/', suppliers.add_supplier , name="addsupplier"),
    path('editsupplier/<int:id>', suppliers.edit_supplier , name="editsupplier"),
    path('deletesupplier/<int:id>', suppliers.delete_supplier , name="deletesupplier"),

# Customers
    path('customers/', customers.customer , name="customers"),
    path('add_customer/', customers.add_customer , name="addcustomer"),
    path('customer/<int:id>', customers.edit_customer , name="editcustomer"),
    path('deletecustomer/<int:id>', customers.delete_customer , name="deletecustomer"),

# Cheques
    path('cheques/', cheques.cheque , name="cheques"),
    path('add_cheque/', cheques.add_cheque , name="addcheque"),
    path('cheque/<int:id>', cheques.edit_cheque , name="editcheque"),
    path('deletecheque/<int:id>', cheques.delete_cheque , name="deletecheque"),

# Gatepass
    # path('gatepass/', gatepass.gatepass , name="gatepass"),
    path('create-gatepass/', gatepass.create_gatepass, name='create_gatepass'),
    path('create-gatepass/', gatepass.create_gatepass, name='create_gatepass'),
    path('edit-gatepass/<int:gatepass_id>/', gatepass.edit_gatepass, name='edit_gatepass'),
    path('cancel_gatepass/<int:id>/', gatepass.cancel_gatepass, name='cancel_gatepass'),
    path('delete_gatepass/<int:id>/', gatepass.delete_gatepass, name='delete_gatepass'),
    path('delete_gatepass_item/<int:id>/', gatepass.delete_gatepass_item, name='delete_gatepass_item'),
    path('list-gatepasses/', gatepass.list_gatepasses, name='list_gatepasses'),
    path('print-gatepass/<int:gatepass_id>/', gatepass.print_gatepass, name='print_gatepass'),

# Sales
    path('list-sales/', sales.list_sales, name='list_sales'),
    path('salereceipt/', sales.salereceipt , name="salereceipt"),
    path('create-salereceipt/', sales.create_salereceipt, name='create_salereceipt'),
    path('create-salereceipt/<int:salereceipt_id>/', sales.create_salereceipt, name='create_salereceipt'),
    path('edit-salereceipt/<int:id>/', sales.edit_salereceipt, name='edit_salereceipt'),
    
    path('create-cash-salereceipt/', sales.create_cash_salereceipt, name='create_cash_salereceipt'),
    path('create-cash-salereceipt/<int:salereceipt_id>/', sales.create_cash_salereceipt, name='create_cash_salereceipt'),
    path('edit-cash-salereceipt/<int:id>/', sales.edit_cash_salereceipt, name='edit_cashsale_receipt'),
    path('cancel_salereceipt/<int:id>/', sales.cancel_salereceipt, name='cancel_salereceipt'),
    path('delete_salereceipt/<int:id>/', sales.delete_salereceipt, name='delete_salereceipt'),
    path('delete_salereceipt_item/<int:id>/', sales.delete_salereceipt_item, name='delete_salereceipt_item'),
    path('print-salereceipt/<int:salereceipt_id>/', sales.print_salereceipt, name='print_salereceipt'),
    path('make_transaction/<int:id>/', sales.make_transaction, name='maketransaction'),

# Get Stock for Issue and Sales
    path('get-stock/<int:id>/', store_issue.get_stock, name='get-stock'),
    path('get-stock-final-product/<int:id>/', sales.get_final_product_stock, name='getstockfinalproduct'),

# Store Issue request

    path('list-store-issue-request/', store_issue_request.list_store_issue_request, name='list_store_issue_request'),
    path('create-store-issue-request/', store_issue_request.create_store_issue_request, name='create_store_issue_request'),
    path('edit-store-issue-request/<int:issue_request_id>/', store_issue_request.edit_store_issue_request, name='edit_store_issue_request'),
    path('store-issuerequest-issuenote/<int:issue_request_id>/', store_issue_request.store_issuerequest_issuenote, name='store_issuerequest_issuenote'),
    path('print-store-issue-request/<int:issue_request_id>/', store_issue_request.print_store_issue, name='print_store_issue_request'),
    path('delete-store-issue-request/<int:id>/', store_issue_request.delete_store_issue_request, name='delete_store_issue_request'),

# Store Issue
    
    path('list-store-issue/', store_issue.list_store_issue, name='list_store_issue'),
    path('create-store-issue/', store_issue.create_store_issue_note, name='create_store_issue'),
    path('edit-store-issue/<int:issue_note_id>/', store_issue.edit_store_issue_note, name='edit_store_issue'),
    path('print-store-issue/<int:issue_note_id>/', store_issue.print_store_issue, name='print_store_issue'),
    path('delete-store-issue/<int:id>/', store_issue.delete_store_issue, name='delete_store_issue_note'),

# Final Product Note
    path('list-final-pro-note/', final_product_note.list_final_product_note, name='list_final_pro_note'),
    path('create-final-pro-note/', final_product_note.create_final_product_note, name='create_final_pro_note'),
    path('edit-final-pro-note/<int:id>', final_product_note.edit_final_product_note, name='edit_final_pro_note'),
    path('delete-final-pro-note/<int:id>', final_product_note.delete_final_product_note, name='delete_final_pro_note'),
    path('print-final-pro-note/<int:id>', final_product_note.print_final_product_note, name='print_final_pro_note'),

# store purchase
    path('list-store-purchase/', store_purchase.list_store_purchase, name='list_store_purchase'),
    path('create-store-purchase/', store_purchase.create_store_purchase, name='create_store_purchase'),
    # path('create-store-purchase/<int:salereceipt_id>/', store_purchase.create_store_purchase, name='create_store_purchase'),
    path('edit-store-purchase/<int:salereceipt_id>/', store_purchase.edit_store_purchase, name='edit_store_purchase'),
    # path('cancel-strore-purchase/<int:id>/', store_purchase.cancel_store_purchase, name='cancel_strore_purchase'),
    path('delete_store_purchase_item/<int:id>/', store_purchase.delete_store_purchase_item, name='delete_store_purchase_item'),
    path('print-store-purchase/<int:salereceipt_id>/', store_purchase.print_store_purchase, name='print_store_purchase'),
    path('delete-store-purchase/<int:id>/', store_purchase.delete_store_purchase, name='delete_store_purchase_note'),

# Accounts
    path('accounts/', accounts.accounts , name="accounts"),
    path('create_accounts/', accounts.create_accounts , name="createaccounts"),
    path('add_account/', accounts.add_account , name="add_accounts"),
    path('editaccount/<int:id>', accounts.edit_account , name="editaccount"),
    path('deleteaccount/<int:id>', accounts.delete_account , name="deleteaccount"),
    path('accountreport/<int:id>', accounts.account_report , name="accountreport"),
    path('account-statement/', accounts.account_statement, name='account_statement'),

# Transactions
    path('list_transactions/', accounts.list_transaction , name="listtransactions"),
    path('transaction/', accounts.add_transaction , name="transaction"),
    path('edittransaction/<int:id>', accounts.edit_transaction , name="edittransaction"),
    path('deletetransaction/<int:id>', accounts.delete_transaction , name="deletetransaction"),
    path('balance_sheet/', accounts.balance_sheet , name="balancesheet"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
