from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from company.models import Worker, Task, Position, TaskType


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    date_hierarchy = "tasks__deadline"
    list_editable = ("is_staff",)
    list_display_links = ("username",)
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "is_completed", "priority")
    list_editable = ("is_completed", "priority")
    search_fields = ("name",)
    list_filter = ("priority", "is_completed")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


admin.site.register(TaskType)
