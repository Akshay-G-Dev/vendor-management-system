import json
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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['items'] = json.loads(str(instance.items).replace("'", '"'))
        return representation

    class Meta:
        model = PurchaseOrder
        fields = [
            "po_id",
            "vendor_reference",
            "order_date",
            "expected_delivery_date",
            "delivered_date",
            "delivered",
            "items",
            "total_quantity",
            "status",
            "amount",
            
        ]
        read_only_fields = ["total_quantity"]
        