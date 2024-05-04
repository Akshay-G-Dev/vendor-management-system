from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from django.db.models import Avg, F


@receiver(pre_save, sender=PurchaseOrder)
def po_handler(sender, instance, **kwargs):
    if instance.id is None:
        pass

    else:
        vendor = instance.vendor_reference
        old_instance = PurchaseOrder.objects.get(id=instance.id)
        if instance.acknowledgment_date != old_instance.acknowledgment_date:
            response_time = PurchaseOrder.objects.filter(
                Q(vendor_reference=vendor) & Q(acknowledgment_date__isnull=False)
            ).aggregate(response_time=Avg(F("acknowledgment_date") - F("issue_date")))[
                "response_time"
            ]
            response_time /= timedelta(days=1)
            print(response_time)
            vendor.average_response_time = str(response_time)
        fulfilled_order = PurchaseOrder.objects.filter(
            Q(vendor_reference=vendor) and Q(status="completed")
        ).count()
        issued_order = PurchaseOrder.objects.filter(Q(vendor_reference=vendor)).count()
        vendor.fulfillment_rate = fulfilled_order / issued_order

        if instance.status == "completed" and old_instance.status != "completed":
            vendor = instance.vendor_reference
            on_time = PurchaseOrder.objects.filter(
                Q(vendor_reference=vendor)
                & Q(status="completed")
                & Q(delivery_date__lte=instance.delivery_date)
            ).count()
            total = PurchaseOrder.objects.filter(
                Q(vendor_reference=vendor) & Q(status="completed")
            ).count()
            if total and on_time:
                vendor.on_time_delivery_rate = on_time / total

            if instance.quality_rating:
                if not vendor.quality_rating_avg:
                    vendor.quality_rating_avg = instance.quality_rating
                else:
                    vendor.quality_rating_avg = (
                        int(vendor.quality_rating_avg or 0) + instance.quality_rating
                    ) / 2
            HistoricalPerformance.objects.update_or_create(
                vendor=vendor,
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            )
        print("s9ignal called")
        vendor.save()
