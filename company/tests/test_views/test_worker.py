from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.forms import WorkerCreationForm
from company.models import Position

WORKERS_URL = reverse("company:worker-list")


class PublicWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test position"
        )
        self.worker = get_user_model().objects.create_user(
            username="test user",
            password="test12345",
            position=self.position
        )

    def test_login_required_workers(self):
        response = self.client.get(WORKERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_worker_detail_login_required(self):
        response = self.client.get(reverse(
            "company:worker-detail", kwargs={"pk": self.worker.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_login_required(self):
        response = self.client.get(reverse(
            "company:worker-update", kwargs={"pk": self.worker.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_login_required(self):
        response = self.client.get(reverse("company:worker-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test_position"
        )
        self.worker = get_user_model().objects.create_user(
            username="test_user",
            password="password111",
            position=self.position,
        )
        self.client.force_login(self.worker)

    def test_retrieve_workers(self):
        for worker_id in range(2, 4):
            position = Position.objects.create(
                name=f"test position{worker_id}"
            )
            get_user_model().objects.create_user(
                username=f"worker{worker_id}",
                password=f"worker1234{worker_id}",
                position=position,
            )

        response = self.client.get(WORKERS_URL)

        workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "company/worker_list.html")

    def test_worker_detail_login_required(self):
        response = self.client.get(reverse(
            "company:worker-detail", kwargs={"pk": self.worker.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_worker_create_login_required(self):
        response = self.client.get(reverse("company:worker-create"))

        self.assertEqual(response.status_code, 200)

    def test_worker_update_login_required(self):
        response = self.client.get(reverse(
            "company:worker-update", kwargs={"pk": self.worker.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_search_worker_form(self):

        response = self.client.get(
            reverse("company:worker-detail",
                    kwargs={"pk": self.worker.id}
                    ) + "?username=user"
        )

        self.assertContains(
            response,
            "user"
        )
        self.assertNotContains(
            response,
            "Paul"
        )

    def test_get_absolute_url(self):
        worker = get_user_model().objects.get(id=1)

        self.assertEqual(
            worker.get_absolute_url(),
            reverse("company:worker-detail",
                    kwargs={"pk": self.worker.id})
        )

    def test_create_worker(self):
        form_data = {
            "username": "new_worker",
            "password1": "worker12test",
            "password2": "worker12test",
            "first_name": "First",
            "last_name": "Last",
            "position": self.position
        }
        self.form = WorkerCreationForm(form_data)
        print(self.form.is_valid())
        print(form_data)
        # print(self.client)
        print(self.client.post(reverse("company:worker-create"), data=form_data))
        # response = self.client.get(reverse("company:worker-create"))
        # self.assertEqual(response.status_code, 200)
        # self.client.force_login(self.user)
        self.client.post(reverse("company:worker-create"), data=form_data)
        print(form_data["username"])
        # self.assertEqual(response.status_code, 200)
        # new = get_user_model().objects.all()
        # print(new)
        new_worker = get_user_model().objects.get(username=form_data["username"])
        # print(new_worker)
        # self.assertEqual(new_worker.username, form_data["username"])
        # self.assertEqual(new_worker.first_name, form_data["first_name"])
        # self.assertEqual(new_worker.last_name, form_data["last_name"])
