from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


def validate_deadline(deadline):
    today = now()
    if (deadline.month - today.month) < 1:
        raise ValidationError("Give it at least a month")


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("company:task-type-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    @staticmethod
    def print_status(position: bool) -> str:
        return "Yes" if position else "No"

    @property
    def print_active(self) -> str:
        return self.print_status(self.is_active)

    @property
    def print_staff(self) -> str:
        return self.print_status(self.is_staff)

    def get_absolute_url(self) -> str:
        return reverse("company:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("A", "URGENT"),
        ("B", "HIGHLY URGENT"),
        ("C", "SLOWLY")
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField(validators=[validate_deadline])
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="A"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True
    )

    class Meta:
        ordering = ["-deadline"]

    def __str__(self) -> str:
        return f"{self.name} {self.task_type.name}"

    @property
    def print_completed(self) -> str:
        return "Done" if self.is_completed else "In work"

    def get_absolute_url(self) -> str:
        return reverse("company:task-detail", kwargs={"pk": self.pk})
