from django.urls import path

from company.views import (
    IndexView,
    TaskTypeListView,
    PositionListView,
    TaskListView,
    WorkerListView,
)

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index"
    ),
    path(
        "tasks-types/",
        TaskTypeListView.as_view(),
        name="task-types-list"
    ),
    path(
            "positions/",
            PositionListView.as_view(),
            name="position-list"
        ),
    path(
            "tasks/",
            TaskListView.as_view(),
            name="task-list"
        ),
    path(
            "workers/",
            WorkerListView.as_view(),
            name="worker-list"
        ),
]

app_name = "company"
