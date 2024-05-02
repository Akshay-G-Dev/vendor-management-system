from django.db import models
from django.core.validators import RegexValidator
import json
from datetime import timedelta

from rest_framework.response import Response

ORDER_STATUS = (
    ("pending", "pending"),
    ("completed", "completed"),
    ("canceled", "canceled"),
)
"""
Fields:
● name: CharField - Vendor's name.
● contact_details: TextField - Contact information of the vendor.
● address: TextField - Physical address of the vendor.
● vendor_code: CharField - A unique identifier for the vendor.
● on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
● quality_rating_avg: FloatField - Average rating of quality based on purchase
orders.
● average_response_time: FloatField - Average time taken to acknowledge
purchase orders.
● fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully."""

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=200, unique=True)
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.FloatField(default=None, null=True)
    fulfillment_rate = models.FloatField(default=None, null=True)

    def __str__(self):
        return self.name + " - " + str(self.vendor_code)


"""Fields:
● po_number: CharField - Unique number identifying the PO.
● vendor: ForeignKey - Link to the Vendor model.
● order_date: DateTimeField - Date when the order was placed.
● delivery_date: DateTimeField - Expected or actual delivery date of the order.
● items: JSONField - Details of items ordered.
● quantity: IntegerField - Total quantity of items in the PO.
● status: CharField - Current status of the PO (e.g., pending, completed, canceled).
● quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
● issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
● acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor
acknowledged the PO."""


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=200, unique=True)
    vendor_reference = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Enter vendor id",
        related_name="purchase_orders",
    )
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
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
    quality_rating = models.FloatField(default=None, null=True, blank=True)
    issue_date = models.DateField(auto_now_add=True)
    acknowledgment_date = models.DateField(null=True)


"""
This model optionally stores historical data on vendor performance, enabling trend analysis.
● Fields:
● vendor: ForeignKey - Link to the Vendor model.
● date: DateTimeField - Date of the performance record.
● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
● quality_rating_avg: FloatField - Historical record of the quality rating average.
● average_response_time: FloatField - Historical record of the average response
time.
● fulfillment_rate: FloatField - Historical record of the fulfilment rate."""

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performance"
    )
    date = models.DateField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=None, null=True, blank=True)
    quality_rating_avg = models.FloatField(default=None, null=True, blank=True)
    average_response_time = models.FloatField(default=None, null=True, blank=True)
    fulfillment_rate = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return self.vendor.name + " - " + str(self.date)