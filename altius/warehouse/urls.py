from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'administrative-units', AdministrativeUnitViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'inventory-items', InventoryItemViewSet)
router.register(r'batches', BatchViewSet)
router.register(r'parties', PartyViewSet)
router.register(r'transactions', TransactionViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path('manage/', include(router.urls))
]