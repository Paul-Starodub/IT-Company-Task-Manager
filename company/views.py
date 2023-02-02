from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from company.models import TaskType, Position, Worker, Task


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

        if "num_visits" in self.request.session:
            self.request.session["num_visits"] += 1
        else:
            self.request.session["num_visits"] = 1

        context["num_visits"] = self.request.session.get("num_visits", 1)

        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    """Class for viewing the list of task types on the site"""

    model = TaskType
    template_name = "company/task_types_list.html"
    context_object_name = "task_types_list"
    paginate_by = 15


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


class PositionListView(LoginRequiredMixin, generic.ListView):
    """Class for viewing the list of positions on the site"""

    model = Position
    paginate_by = 20


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about position on the site """

    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    """Class for creating a new position"""

    model = Position
    fields = "__all__"
    success_url = reverse_lazy("company:position-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    """Class for viewing the list of tasks on the site"""

    model = Task
    paginate_by = 10


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about task on the site """

    model = Task


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """Class for viewing the list of workers on the site"""

    queryset = Worker.objects.select_related("position")
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    """Class for viewing the detail information about worker on the site """

    model = Worker
