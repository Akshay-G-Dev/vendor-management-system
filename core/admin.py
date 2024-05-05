from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.admin import SimpleListFilter


class IsVendor(SimpleListFilter):
    title = "Vendor"
    parameter_name = "Vendor"

    def lookups(self, request, model_admin):
        return [(1, "Vendor"), (0, "Not Vendor")]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(vendor_profile__isnull=False)
        if self.value() == "0":
            return queryset.filter(vendor_profile__isnull=True)

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

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', "vendor_profile")
    search_fields = ('username', 'email', 'first_name', 'last_name', "vendor_profile__name","vendor_profile__vendor_code")
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',IsVendor)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',"vendor_profile")}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',"vendor_profile"),
        }),
    )

admin.site.register(User, CustomUserAdmin)
