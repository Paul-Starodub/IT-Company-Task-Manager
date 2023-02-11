from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from company.models import Position, TaskType, Task


class PositionTaskTypeTests(TestCase):

    def test_position_str(self):
        position = Position.objects.create(
            name="test",
        )

        self.assertEqual(
            str(position),
            position.name
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="test"
        )

        self.assertEqual(
            str(task_type),
            task_type.name
        )

    def test_task_type_get_absolute_url(self):
        task_type = TaskType.objects.create(
            name="test12345",
        )

        self.assertEqual(
            task_type.get_absolute_url(),
            reverse("company:task-type-detail", kwargs={"pk": task_type.id})
        )


class TaskTests(TestCase):
    def setUp(self) -> None:
        task_type = TaskType.objects.create(
            name="test"
        )
        self.task = Task.objects.create(
            name="test12345",
            description="About task",
            deadline=now(),
            task_type=task_type
        )

    def test_task_str(self):

        self.assertEqual(
            str(self.task),
            f"{self.task.name} {self.task.task_type.name}"
        )

    def test_task_deadline(self):

        self.assertRaises(ValidationError, self.task.full_clean)

    def test_task_get_absolute_url(self):

        self.assertEqual(
            self.task.get_absolute_url(),
            reverse("company:task-detail", kwargs={"pk": self.task.id})
        )

    def test_task_property(self):
        self.assertEqual(self.task.completed, "In work")


class WorkerTests(TestCase):
    def setUp(self) -> None:
        self.username = "test"
        self.password = "test12345"
        self.position = Position.objects.create(
            name="test",
        )
        self.worker = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            position=self.position,
            is_staff=True
        )

    def test_worker_get_absolute_url(self):

        self.assertEqual(
            self.worker.get_absolute_url(),
            reverse("company:worker-detail", kwargs={"pk": self.worker.id})
        )

    def test_worker_str(self):

        self.assertEqual(
            str(self.worker),
            f"{self.worker.username} "
            f"({self.worker.first_name} {self.worker.last_name})"
        )

    def test_create_worker(self):

        self.assertEqual(self.worker.username, self.username)
        self.assertTrue(self.worker.check_password(self.password))
        self.assertEqual(self.worker.position, self.position)

    def test_worker_properties(self):

        self.assertEqual(self.worker.staff, "Yes")
        self.assertEqual(self.worker.active, "Yes")
