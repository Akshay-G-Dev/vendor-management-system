import json
import re
from pkg_resources import require
from rest_framework import serializers
from .models import Vendor, PurchaseOrder
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    vendor_code = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
            "vendor_code"
            
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {"detail": "User Already exist!"}
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance["password"] != instance["password2"]:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=instance["email"]).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop("password")
        passowrd2 = validated_data.pop("password2")
        vendor_code = None
        if "vendor_code" in validated_data:
            vendor_code = validated_data.pop("vendor_code")

        user = User.objects.create(**validated_data)
        user.set_password(passowrd)
        if vendor_code:
            try:
                vendor = Vendor.objects.get(vendor_code__iexact=vendor_code)
                user.vendor_profile = vendor
                
            except Vendor.DoesNotExist:
                raise ValidationError({"message": "Vendor does not exist with this vendor code!"})

        user.save()
        Token.objects.create(user=user)
        return user


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
