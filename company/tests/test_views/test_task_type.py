from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import TaskType, Position

TASK_TYPES_URL = reverse("company:task-types-list")


class PublicTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test task type",
        )

    def test_task_type_list_login_required(self):
        response = self.client.get(TASK_TYPES_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        response = self.client.get(reverse("company:task-type-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_update_login_required(self):
        response = self.client.get(reverse(
            "company:task-type-update", kwargs={"pk": self.task_type.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_delete_login_required(self):
        response = self.client.get(reverse(
            "company:task-type-delete", kwargs={"pk": self.task_type.id}
        ))

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="first_task_type"
        )
        number_of_task_types = 20

        for task_type in range(2, number_of_task_types):
            TaskType.objects.create(
                name=f"{task_type}name",
            )

        self.queryset = TaskType.objects.all()
        self.position = Position.objects.create(name="Try")
        self.worker = get_user_model().objects.create_user(
            username="test",
            password="password123",
            position=self.position
        )
        self.client.force_login(self.worker)

    def test_task_type_list_login_required(self):
        response = self.client.get(TASK_TYPES_URL)

        self.assertEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        response = self.client.get(reverse("company:task-type-create"))

        self.assertEqual(response.status_code, 200)

    def test_task_type_update_login_required(self):
        response = self.client.get(reverse(
            "company:task-type-update", kwargs={"pk": self.task_type.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_task_type_delete_login_required(self):
        response = self.client.get(reverse(
            "company:task-type-delete", kwargs={"pk": self.task_type.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_task_types(self):
        response = self.client.get(TASK_TYPES_URL)

        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(self.queryset),
            list(task_types)
        )
        self.assertTemplateUsed(
            response,
            "company/task_types_list.html"
        )

    def test_pagination_is_six(self):
        response = self.client.get(TASK_TYPES_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_types_list"]), 15)
