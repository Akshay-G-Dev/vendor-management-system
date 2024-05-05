from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {"username": {"detail": "User Doesnot exist!"}}
            if User.objects.filter(username=request.data["username"]).exists():
                user = User.objects.get(username=request.data["username"])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "success": True,
                    "username": user.username,
                    "email": user.email,
                    "token": token.key,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "user": serializer.data,
                "token": Token.objects.get(
                    user=User.objects.get(username=serializer.data["username"])
                ).key,
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK
        )


class VendorSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        return Response(
            {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }
        )


class IsSameVendor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.vendor_reference == request.user.vendor_profile


class PurchaseOrderSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated] #IsSameVendor

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        
        po = self.get_object()
        if po.vendor_reference == request.user.vendor_profile:
            po.acknowledgment_date = timezone.now()
            if request.data.get("quality_rating"):
                po.quality_rating = request.data["quality_rating"]
            po.save()
            return Response({"message": "Acknowledged"})
        else:
            return Response({"message": "Unauthorized. Only reference vendor can acknowledge it"}, status=status.HTTP_401_UNAUTHORIZED)
