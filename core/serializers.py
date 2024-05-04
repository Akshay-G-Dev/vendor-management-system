import json
from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Vendor
        fields = "__all__"

class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['items'] = json.loads(str(instance.items).replace("'", '"'))
        return representation
    

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = ["quantity"]
        