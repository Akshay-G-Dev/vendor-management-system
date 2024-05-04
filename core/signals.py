from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from django.db.models import Avg, F


@receiver(pre_save, sender=PurchaseOrder)
def po_handler(sender, instance, **kwargs):

    if instance.id is None:
        try:
            instance.quantity = sum(map(int, json.loads(instance.items).values()))
        except:
            instance.quantity = 0
            raise ValueError("Invalid Values for quantity")

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
        if instance.items != old_instance.items:
            try:
                instance.quantity = sum(map(int, json.loads(instance.items).values()))
            except:
                instance.quantity = 0
            raise ValueError("Invalid Values for quantity")
        if instance.status == "completed" and old_instance.status != "completed":
            vendor = instance.vendor_reference

            on_time = (
                PurchaseOrder.objects.filter(
                    Q(vendor_reference=vendor)
                    & Q(status="completed")
                    & Q(delivery_date__lte=instance.delivery_date)
                ).count()
                + 1
            )
            total = (
                PurchaseOrder.objects.filter(
                    Q(vendor_reference=vendor) & Q(status="completed")
                ).count()
                + 1
            )

            if total and on_time:
                vendor.on_time_delivery_rate = on_time / total

            if instance.quality_rating:
                if not vendor.quality_rating_avg:
                    vendor.quality_rating_avg = instance.quality_rating
                else:
                    vendor.quality_rating_avg = (
                        vendor.quality_rating_avg + instance.quality_rating
                    ) / 2

        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def po_after_save_handler(sender, instance, **kwargs):
    vendor = instance.vendor_reference
    fulfilled_order = PurchaseOrder.objects.filter(
        Q(vendor_reference=vendor) and Q(status="completed")
    ).count()
    issued_order = PurchaseOrder.objects.filter(Q(vendor_reference=vendor)).count()
    vendor.fulfillment_rate = fulfilled_order / issued_order
    vendor.save()


@receiver(post_save, sender=Vendor)
def vendor_after_save_handler(sender, instance, **kwargs):
    vendor = instance
    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate,
    )
