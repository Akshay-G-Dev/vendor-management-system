from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Vendor
        fields = [
            "vendor_id",
            "name",
            "phone",
            "email",
            "address",
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = PurchaseOrder
        fields = [
            "po_id",
            "vendor_reference",
            "order_date",
            "items",
            "total_quantity",
            "status",
        ]
