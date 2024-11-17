from django.db import models

# Create your models here.
from django.db import models
from django.db import IntegrityError
from django.utils.timezone import now
from django.core.exceptions import ValidationError

import hashlib


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


class AdministrativeUnit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{str(self.id)} - {self.name}"


class Location(models.Model):
    administrative_unit = models.ForeignKey(
        AdministrativeUnit, on_delete=models.CASCADE, default=1
    )
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[("warehouse", "Warehouse"), ("storefront", "Storefront")],
        default="warehouse",
    )

    def __str__(self):
        return f"{str(self.id)} - {self.administrative_unit.name} - {self.type}"



class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.batch.party} - {self.batch.receiving_date}"

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # if is_new:
        #     warehouse_location = Location.objects.filter(
        #         administrative_unit=self.administrative_unit, type="warehouse"
        #     ).first()

        #     if warehouse_location:
        #         Reception.objects.create(
        #             inventory_item=self,
        #             batch=self.batch,
        #             location=warehouse_location,
        #             quantity=self.quantity,
        #             date=now().date(),
        #             user=user,
        #         ) 

    def add_stock(id, quantity,location, user=None,):
        self = InventoryItem.objects.get(id=id,location=location)
        self.quantity += quantity
        self.save()


    def remove_stock(id, quantity, location, user=None):
        self = InventoryItem.objects.get(id=id, location=location)
        if self.quantity < quantity:
            raise ValidationError("Cannot remove more stock than available.")
        self.quantity -= quantity
        self.save()

    def transfer_stock(id, quantity, origin, target, user=None):
        self = InventoryItem.objects.get(id=id, location=origin)
        target_inventory_item = InventoryItem.objects.get(id=id, location=target)
        if self.quantity < quantity:
            raise ValidationError("Cannot transfer more stock than available.")
        self.remove_stock(id, quantity, origin, user)
        target_inventory_item.add_stock(id, quantity, target, user)
        

class Batch(models.Model):  # Renamed from ReceptionBatch
    receiving_date = models.DateField()
    party = models.ForeignKey(
        "Party", on_delete=models.CASCADE
    )  # Changed from supplier
    total_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    receiptID = models.CharField(max_length=50, unique=True)
    type = models.CharField(
        max_length=10, choices=[("reception", "Reception"), ("dispatch", "Dispatch")]
    )

    def __str__(self):
        return f"{self.party} - {self.receiving_date} - {self.type}"


class Party(models.Model):  # Renamed from Supplier
    name = models.CharField(max_length=255)
    address = models.TextField(default="")
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    tax_id = models.CharField(max_length=50)
    type = models.CharField(
        max_length=10, choices=[("supplier", "Supplier"), ("receiver", "Receiver")]
    )

    def __str__(self):
        return f"{self.name} - {self.type}"



class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location_to = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_to")
    location_from = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="location_from"
    )
    quantity = models.IntegerField()
    party  = models.ForeignKey(Party, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    state = models.CharField(
        max_length=50,
        choices=[
            ("issued","Issued"),
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    notes = models.TextField(blank=True, null=True)

    operation = models.CharField(
        max_length=10, choices=[("reception", "Reception"), ("dispatch", "Dispatch")]
    )


