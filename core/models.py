from django.db import models
from django.core.validators import RegexValidator

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
