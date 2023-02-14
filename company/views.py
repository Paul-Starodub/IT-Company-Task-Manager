from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from company.forms import (
    TaskUpdateForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    WorkerSearchForm
)
from company.models import (
    TaskType,
    Position,
    Worker,
    Task
)
from company.utils import SearchMixin


class IndexView(LoginRequiredMixin, generic.TemplateView):
    """Class for viewing the home page on the site"""

    template_name = "company/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        home_context = {
            "current_time": datetime.now(),
            "num_task_types": TaskType.objects.count(),
            "num_positions": Position.objects.count(),
            "num_workers": Worker.objects.count(),
            "num_tasks": Task.objects.count()
        }

        context.update(home_context)

        self.request.session["num_visits"] = self.request.session.get(
            "num_visits", 0
        ) + 1
        context["num_visits"] = self.request.session.get("num_visits", 1)

        return context


class TaskTypeListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    """Class for viewing the list of task types on the site"""

    template_name = "company/task_types_list.html"
    context_object_name = "task_types_list"
    paginate_by = 15
    class_name = TaskType


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about task type on the site """

    model = TaskType
    context_object_name = "task_type"
    template_name = "company/task_type_detail.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    """Class for creating a new type task"""

    model = TaskType
    fields = "__all__"
    template_name = "company/task_type_form.html"
    success_url = reverse_lazy("company:task-types-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Class for updating task type"""

    model = TaskType
    fields = "__all__"
    template_name = "company/task_type_form.html"
    success_url = reverse_lazy("company:task-types-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Class for delete task type"""

    model = TaskType
    success_url = reverse_lazy("company:task-types-list")
    template_name = "company/task_type_confirm_delete.html"


class PositionListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    """Class for viewing the list of positions on the site"""

    paginate_by = 20
    class_name = Position


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about position on the site """

    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    """Class for creating a new position"""

    model = Position
    fields = "__all__"
    success_url = reverse_lazy("company:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Class for updating position"""

    model = Position
    fields = "__all__"
    success_url = reverse_lazy("company:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Class for delete position"""

    model = Position
    success_url = reverse_lazy("company:position-list")


class TaskListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    """Class for viewing the list of tasks on the site"""

    paginate_by = 10
    class_name = Task

    def get_queryset(self):
        self.queryset = super().get_queryset()

        if "is_completed" in self.request.GET.keys():
            return self.queryset.filter(
                is_completed=self.request.GET["is_completed"]
            )

        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about task on the site """

    model = Task

    def get_context_data(self, **kwargs):  # reduce the load on the database
        context = super().get_context_data(**kwargs)
        context["task_workers"] = self.object.assignees.all()
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Class for creating a new task"""

    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type")
    success_url = reverse_lazy("company:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Class for update task"""

    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("company:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Class for delete task"""

    model = Task
    success_url = reverse_lazy("company:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """Class for viewing the list of workers on the site"""

    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name_user = self.request.GET.get("name_user", "")
        context["search_form"] = WorkerSearchForm(
            initial={
                "name_user": name_user
            }
        )

        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        queryset = Worker.objects.select_related("position")

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["name_user"]
            )

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about worker on the site """

    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    """Class for creating a new worker"""

    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Class for update position of worker"""

    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("company:worker-list")


class WorkerTaskListView(LoginRequiredMixin, generic.ListView):
    """Class for assigning a worker to a task"""

    model = Task
    fields = "__all__"
    success_url = reverse_lazy("company:task-list")

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        worker = get_object_or_404(Worker, pk=self.request.user.pk)
        if worker not in task.assignees.all():
            task.assignees.add(worker)
        else:
            task.assignees.remove(worker)
        return HttpResponseRedirect(
            reverse("company:task-detail", kwargs={"pk": self.kwargs["pk"]})
        )


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Class for delete the worker"""

    model = Worker
    success_url = reverse_lazy("company:worker-list")
