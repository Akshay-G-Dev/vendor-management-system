from django.shortcuts import render
from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer


class VendorSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

