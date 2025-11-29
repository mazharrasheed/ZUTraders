from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from .models import Store_Purchase_Product, Store_Issue_Product, Inventory
from django.db.models.signals import post_save
from .models import Transaction


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


from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from decimal import Decimal

@receiver(pre_save, sender=Transaction)
def before_transaction_saved(sender, instance, **kwargs):
    if instance.pk:
        old = Transaction.objects.get(pk=instance.pk)
        instance._old_amount = old.amount
    else:
        instance._old_amount = Decimal("0")

@receiver(post_save, sender=Transaction)
def after_transaction_saved(sender, instance, created, **kwargs):

    # Identify cheque account
    cheque = None
    if hasattr(instance.debit_account, "cheque") and instance.debit_account.cheque:
        cheque = instance.debit_account.cheque
    elif hasattr(instance.credit_account, "cheque") and instance.credit_account.cheque:
        cheque = instance.credit_account.cheque

    if not cheque:
        return

    # ---- NEW TRANSACTION ----
    if created:
        diff = instance.amount  # Positive
        cheque.apply_payment(diff)
        return

    # ---- UPDATED TRANSACTION ----
    old_amount = Decimal(getattr(instance, "_old_amount", 0))
    new_amount = instance.amount

    diff = new_amount - old_amount     # may be positive or negative

    if diff != 0:
        cheque.apply_payment(diff)
