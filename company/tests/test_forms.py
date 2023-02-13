import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from company.forms import WorkerCreationForm, TaskUpdateForm
from company.models import Position, TaskType, Task


class WorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test position"
        )
        self.worker = get_user_model().objects.create_user(
            username="new_worker",
            password="user123test",
            position=self.position
        )
        self.form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": self.position
        }
        self.form = WorkerCreationForm(data=self.form_data)

    def test_worker_creation_form_with_position_is_valid(self):

        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_worker_creation_form_with_not_expected_position(self):
        self.form_data["position"] = "QA"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test tsk type"
        )
        self.position = Position.objects.create(
            name="test position"
        )
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker12345",
            position=self.position
        )
        self.task = Task.objects.create(
            name="test12345",
            description="About task",
            deadline=(datetime.date.today() + datetime.timedelta(weeks=5)),
            priority="Slowly",
            is_completed=False,
            task_type=self.task_type
        )
        self.task.assignees.add(self.worker)
        self.form_data = {
            "description": "About task",
            "priority": "A",
            "is_completed": False,
            "assignees": self.task.assignees.all()
        }

        self.form = TaskUpdateForm(self.form_data)

    def test_task_with_not_expected_description(self):
        self.form_data["description"] = "about task"

        self.assertFalse(self.form.is_valid())
        self.assertTrue(self.form.is_bound)
        self.assertTrue(self.form.cleaned_data)

    def test_task_with_valid_data(self):

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.is_bound)
        self.assertTrue(self.form.cleaned_data)
