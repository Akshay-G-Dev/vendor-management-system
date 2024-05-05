from django.urls import path
from . import views
from rest_framework import routers, serializers, viewsets
from .models import Vendor
from .serializers import VendorSerializer

router = routers.DefaultRouter()
router.register(r"vendors", views.VendorSet)
router.register(r"purchase_orders", views.PurchaseOrderSet)

urlpatterns = router.urls
urlpatterns += [
    path("login/", views.UserLoginAPIView.as_view(), name="user_login"),
    path("register/", views.UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="user_logout")

]
