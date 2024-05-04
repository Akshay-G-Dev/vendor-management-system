from django.test import TestCase
from core.views import VendorSet, PurchaseOrderSet
from core.models import Vendor, PurchaseOrder
from rest_framework.test import APIClient
import json


class TestVendorAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            vendor_code="TV",
            contact_details="testemailaddress@ds.com +91 1234567890",
            address="Test Address",
        )

    def test_vendor_creation(self):
        response = self.client.get(f"/vendors/{self.vendor.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "name": "Test Vendor",
                "vendor_code": "TV",
                "contact_details": "testemailaddress@ds.com +91 1234567890",
                "address": "Test Address",
                "on_time_delivery_rate": None,
                "quality_rating_avg": None,
                "average_response_time": None,
                "fulfillment_rate": None,
            },
        )

    def test_vendor_performance(self):
        response = self.client.get(f"/vendors/{self.vendor.id}/performance/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "on_time_delivery_rate": None,
                "quality_rating_avg": None,
                "average_response_time": None,
                "fulfillment_rate": None,
            },
        )


class PurchaseOrderAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            vendor_code="TV",
            contact_details="testemailaddress@ds.com +91 1234567890",
            address="Test Address",
        )
        self.po = PurchaseOrder.objects.create(
            vendor_reference=self.vendor,
            po_number="PO1",
            order_date="2024-05-04",
            delivery_date="2024-05-15",
            status="pending",
            items=json.dumps(
                {
                    "item1": 10,
                }
            ),
        )

    def test_created_po(self):
        response = self.client.get(f"/purchase_orders/{self.po.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "po_number": "PO1",
                "vendor_reference": self.vendor.id,
                "order_date": "2024-05-04",
                "delivery_date": "2024-05-15",
                "issue_date": "2024-05-04",
                "acknowledgment_date": None,
                "status": "pending",
                "items": {"item1": 10},
                "quantity": 10,
            },
        )

    def test_acknowledge_po(self):
        response = self.client.post(
            f"/purchase_orders/{self.po.id}/acknowledge/", data={"quality_rating": 4}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Acknowledged"})
