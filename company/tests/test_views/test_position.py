from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Position

POSITIONS_URL = reverse("company:position-list")


class PublicPositionTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test position",
        )

    def test_position_list_login_required(self):
        response = self.client.get(POSITIONS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_position_create_login_required(self):
        response = self.client.get(reverse("company:position-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_position_update_login_required(self):
        response = self.client.get(reverse(
            "company:position-update", kwargs={"pk": self.position.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_position_delete_login_required(self):
        response = self.client.get(reverse(
            "company:position-delete", kwargs={"pk": self.position.id}
        ))

        self.assertNotEqual(response.status_code, 200)


class PrivatePositionsTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="first_position"
        )
        number_of_positions = 7

        for position in range(2, number_of_positions):
            Position.objects.create(
                id=position,
                name=f"{position}name",
            )

        self.queryset = Position.objects.all()

        self.worker = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.worker)

    def test_position_list_login_required(self):
        response = self.client.get(POSITIONS_URL)

        self.assertEqual(response.status_code, 200)

    def test_position_create_login_required(self):
        response = self.client.get(reverse("company:position-create"))

        self.assertEqual(response.status_code, 200)

    def test_position_update_login_required(self):
        response = self.client.get(reverse(
            "company:position-update", kwargs={"pk": self.position.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_position_delete_login_required(self):
        response = self.client.get(reverse(
            "company:position-delete", kwargs={"pk": self.position.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_positions(self):
        response = self.client.get(POSITIONS_URL)

        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(self.queryset),
            list(positions)
        )
        self.assertTemplateUsed(
            response,
            "company/position_list.html"
        )

    def test_pagination_is_six(self):
        response = self.client.get(POSITIONS_URL)
        print(response)
        self.assertTrue("is_paginated" in response.context)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["position_list"]), 6)
