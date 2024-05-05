from django.db import models
from django.core.validators import RegexValidator
import json
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from rest_framework.response import Response

ORDER_STATUS = (
    ("pending", "pending"),
    ("completed", "completed"),
    ("canceled", "canceled"),
)

class User(AbstractUser):
    vendor_profile = models.ForeignKey(
        "Vendor", on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=200, unique=True)
    on_time_delivery_rate = models.FloatField(
        default=None, null=True, help_text="Optional"
    )
    quality_rating_avg = models.FloatField(
        default=None, null=True, help_text="Optional"
    )
    average_response_time = models.FloatField(
        default=None, null=True, help_text="Optional"
    )
    fulfillment_rate = models.FloatField(default=None, null=True, help_text="Optional")

    def __str__(self):
        return self.name + " - " + str(self.vendor_code)


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=200, unique=True)
    vendor_reference = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        help_text="Enter vendor id",
        related_name="purchase_orders",
    )
    order_date = models.DateField()
    delivery_date = models.DateField(
        null=True, blank=True, help_text="Expected or Actual Delivery Date"
    )
    items = models.TextField(
        help_text='Enter items in JSON format. Example: {"item1": 10, "item2": 20}'
    )
    quantity = models.IntegerField(
        editable=False, default=0, help_text="Auto Calculated with items"
    )
    status = models.CharField(
        max_length=100,
        help_text="Enter status of the order",
        default="pending",
        choices=ORDER_STATUS,
    )
    quality_rating = models.FloatField(
        default=None, null=True, blank=True, help_text="Optional"
    )
    issue_date = models.DateField(auto_now_add=True)
    acknowledgment_date = models.DateField(null=True, blank=True, help_text="Optional")


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performance"
    )
    date = models.DateField(auto_now=True, help_text="Last Updated")
    on_time_delivery_rate = models.FloatField(default=None, null=True, blank=True)
    quality_rating_avg = models.FloatField(default=None, null=True, blank=True)
    average_response_time = models.FloatField(default=None, null=True, blank=True)
    fulfillment_rate = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return self.vendor.name + " - " + str(self.date)
