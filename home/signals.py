from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Store_Purchase_Product, Store_Issue_Product, Inventory

# 📦 Update Inventory when a product is purchased (add stock)
@receiver(post_save, sender=Store_Purchase_Product)
def update_inventory_on_purchase(sender, instance, created, **kwargs):
   
    product = instance.product
    inventory, created = Inventory.objects.get_or_create(product=product)
    inventory.quantity += int(instance.quantity)  # Add to inventory
    inventory.save()

# 📦 Revert Inventory when a purchase is deleted
@receiver(post_delete, sender=Store_Purchase_Product)
def revert_inventory_on_purchase_delete(sender, instance, **kwargs):
    product = instance.product
    inventory, created = Inventory.objects.get_or_create(product=product)
    inventory.quantity -= int(instance.quantity)  # Subtract from inventory
    if inventory.quantity < 0:  # Ensure no negative quantities
        inventory.quantity = 0
    inventory.save()

# 📦 Update Inventory when a product is issued (deduct stock)
@receiver(post_save, sender=Store_Issue_Product)
def update_inventory_on_issue(sender, instance, created, **kwargs):
    product = instance.product
    inventory, created = Inventory.objects.get_or_create(product=product)
    inventory.quantity -= int(instance.quantity)  # Deduct from inventory
    inventory.save()

# 📦 Revert Inventory when an issue is deleted
@receiver(post_delete, sender=Store_Issue_Product)
def revert_inventory_on_issue_delete(sender, instance, **kwargs):
    product = instance.product
    inventory, created = Inventory.objects.get_or_create(product=product)
    inventory.quantity += int(instance.quantity)  # Add back to inventory
    inventory.save()
