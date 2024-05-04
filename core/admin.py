from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor_code", "contact_details", "address")
    search_fields = ("name", "vendor_code")
    list_filter = ("name", "vendor_code")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "po_number",
        "vendor_reference",
        "order_date",
        "delivery_date",
        "status",
    )
    search_fields = (
        "po_number",
        "vendor_reference__name",
        "vendor_reference__vendor_code",
    )
    list_filter = ("status", "order_date", "delivery_date", "vendor_reference")


@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "vendor",
        "date",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate",
    )
    search_fields = ("vendor__name", "vendor__vendor_code", "date")
    list_filter = (
        "date",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate",
    )
