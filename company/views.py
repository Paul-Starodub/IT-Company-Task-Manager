from datetime import datetime

from django.views import generic

from company.models import TaskType, Position, Worker, Task


class IndexView(generic.TemplateView):
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
