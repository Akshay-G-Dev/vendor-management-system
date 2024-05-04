import json
from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField(
        help_text='Enter items in JSON format. Example: {"item1": 10, "item2": 20}'
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["items"] = json.loads(str(instance.items).replace("'", '"'))
        return representation

    def validate(self, attrs):
        required_fields = ["items", "vendor_reference", "delivery_date"]
        errors = {}
        for field in required_fields:
            if not attrs.get(field):
                errors[field] = "This field may not be blank."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = ["quantity"]
