from django.urls import path
from . import views
from rest_framework import routers, serializers, viewsets
from .models import Vendor
from .serializers import VendorSerializer

router = routers.DefaultRouter()
router.register(r"vendors", views.VendorSet)

urlpatterns = router.urls