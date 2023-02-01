from django.urls import path

from company.views import (
    IndexView,
    TaskTypeListView,
    TaskTypeDetailView,
    PositionListView,
    PositionDetailView,
    TaskListView,
    TaskDetailView,
    WorkerListView,
    WorkerDetailView,
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
        "tasks-types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail"
    ),

    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),

]

app_name = "company"
