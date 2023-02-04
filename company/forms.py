from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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


class TaskUpdateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = ("description", "priority", "is_completed", "assignees")

    def clean_description(self):
        description = self.cleaned_data["description"]
        if not (description[:1].isupper() and description[:1].isalpha()):
            raise ValidationError(
                "First character must be capital letter"
            )
        return description


class NameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
