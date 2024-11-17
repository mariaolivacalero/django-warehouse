from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category__name")
    list_filter = ("category",)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ( "party", "receiving_date")

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity","location")
    search_fields = ("product__name", "location__name")
    list_filter = ("product", "location")

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "administrative_unit", "type")
    search_fields = ("name", "administrative_unit__name")
    list_filter = ("administrative_unit", "type")

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "date", "operation", "state","batch")
    search_fields = ("product__name", "state","operation","batch__party")
    list_filter = ("operation", "state","batch")
