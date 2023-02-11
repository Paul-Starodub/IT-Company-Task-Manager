from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin test",
            password="admin67876",
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Engineer")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker12345",
            position=self.position,
            first_name="Worker",
            last_name="Last",
            email="worker@gmail.com",
            is_staff=False
        )

    def test_worker_position_listed(self):
        """
        Tests that worker's characteristics is in
        list_display on worker admin page
        """
        url = reverse("admin:company_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)
        self.assertContains(response, self.worker.first_name)
        self.assertContains(response, self.worker.last_name)
        self.assertContains(response, self.worker.email)
        self.assertContains(response, self.worker.staff)

    def test_worker_detail_position_listed(self):
        """Tests that worker's position is in worker detail admin page"""
        url = reverse("admin:company_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_add_worker_detail_license_number_listed(self):
        """
        Tests that worker's position, first_name,
        last_name is in worker add admin page
        """
        url = reverse("admin:company_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "position")
