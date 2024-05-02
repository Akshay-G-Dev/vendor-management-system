from django.db import models
from django.core.validators import RegexValidator
import json
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, validators=[RegexValidator(r'^\+?(91)?[6-9]\d{9}$', message="Invalid phone number")])
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            last_vendor = Vendor.objects.order_by('-id').first()
            if last_vendor:
                self.vendor_code = "VE" + str(last_vendor.id + 1)
            else:
                self.vendor_code = "VE1"
        return super(Vendor, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name




class PurchaseOrder(models.Model):
    po_number = models.IntegerField(unique=True, primary_key=True,default=1)
    vendor_reference = models.ForeignKey(
        Vendor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="purchase_orders",
        help_text="Enter vendor id",
    )
    order_date = models.DateField()
    items = models.TextField(help_text="Enter items in JSON format")
    total_quantity = models.IntegerField(editable=False, default=0, help_text="Auto Calculated with items")
    status = models.CharField(max_length=100, help_text="Enter status of the order")
    amount=models.IntegerField(default=None,blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.items:
            print(type(json.loads(self.items)))
            self.total_quantity = sum(json.loads(self.items).values())
            self.items = json.dumps(self.items)
        return super(PurchaseOrder, self).save(*args, **kwargs)
        
    
    
    def __str__(self):
        return self.po_number