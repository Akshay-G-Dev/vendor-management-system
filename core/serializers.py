from rest_framework import serializers 
from .models import Vendor, PurchaseOrder
class VendorSerializer(serializers.ModelSerializer):
    vendor_code = serializers.CharField(read_only=True)
    class Meta:
        model = Vendor
        fields = ["id",'name', 'phone', 'email', 'address', 'vendor_code']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor_reference', 'order_date', 'items', 'total_quantity', 'status']