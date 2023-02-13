from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from company.models import Position, TaskType, Task


class PublicViewsTests(TestCase):

    def test_index_login_required(self):
        response = self.client.get(reverse("company:index"))

        self.assertEqual(response.status_code, 302)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        position = Position.objects.create(name="Test position")
        self.worker = get_user_model().objects.create_user(
            username="user_test_views",
            password="test password",
            position=position,
        )
        self.client.force_login(self.worker)

        for _ in range(1, 4):
            position = Position.objects.create(
                name=f"test_position{_}"
            )

            task_type = TaskType.objects.create(
                name=f"test_type{_}",
            )

            Task.objects.create(
                name=f"test{_}",
                description=f"Test_description{_}",
                deadline="2024-08-07",
                task_type=task_type
            )

            get_user_model().objects.create(
                username=f"test_driver{_}",
                password=f"test_driver_{_}_password",
                position=position
            )

    def test_index_correct_objects_counting(self):
        response = self.client.get(reverse("company:index"))
        all_objects = {
            "num_positions": Position.objects.count(),
            "num_workers": get_user_model().objects.count(),
            "num_task_types": TaskType.objects.count(),
            "num_tasks": Task.objects.count(),
            "num_visits": 1
        }

        self.assertEqual(
            response.context["num_positions"],
            all_objects["num_positions"]
        )
        self.assertEqual(
            response.context["num_workers"],
            all_objects["num_workers"]
        )
        self.assertEqual(
            response.context["num_task_types"],
            all_objects["num_task_types"]
        )
        self.assertEqual(
            response.context["num_tasks"],
            all_objects["num_tasks"]
        )
        self.assertEqual(
            response.context["num_visits"],
            1
        )
