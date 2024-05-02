from django.db import models
from django.core.validators import RegexValidator
import json
from datetime import timedelta

from rest_framework.response import Response
ORDER_STATUS = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
)


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(r"^\+?(91)?[6-9]\d{9}$", message="Invalid phone number")
        ],
    )
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    # vendor_code = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name+" - "+str(self.vendor_id)


class PurchaseOrder(models.Model):
    po_id = models.AutoField(primary_key=True)
    vendor_reference = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_orders",
        help_text="Enter vendor id",
    )
    order_date = models.DateField()
    items = models.TextField(help_text='Enter items in JSON format. Example: {"item1": 10, "item2": 20}')
    total_quantity = models.IntegerField(
        editable=False, default=0, help_text="Auto Calculated with items"
    )
    status = models.CharField(
        max_length=100,
        help_text="Enter status of the order",
        default="pending",
        choices=ORDER_STATUS,
    )
    amount = models.IntegerField(default=None, blank=True, null=True)
    expected_delivery_date = models.DateField()
    delivered_date = models.DateField(default=None, blank=True, null=True)
    delivered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.po_id:
            if not self.expected_delivery_date:
                self.expected_delivery_date = self.order_date + timedelta(days=5)
        if self.items:
            try:
                self.total_quantity = sum(json.loads(self.items).values())
                self.items = json.dumps(json.loads(self.items))
            except Exception as e:
                print(e)
                return Response("Invalid JSON format", status=400)
        return super(PurchaseOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.po_id
