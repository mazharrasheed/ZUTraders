from django.contrib import admin

from .models import Blog,Item_Category,Item,GatePass,GatePassProduct,UnderConstruction

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''

    list_display = ['id','title','description']
   

@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('productname',)

    search_fields = ('productname',)

@admin.register(UnderConstruction)
class UnderConstructionAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('id','is_under_construction','uc_note','uc_duration')

    fields = ('is_under_construction','uc_note','uc_duration')
