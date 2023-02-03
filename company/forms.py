from django import forms
from django.contrib.auth import get_user_model
from company.models import Task, Worker, Position
from django.contrib.auth.forms import UserCreationForm


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "position"
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Worker
        fields = ("position",)


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = ("deadline", "priority", "is_completed", "assignees")
