from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Task


@admin.action(description="Mark selected tasks as Completed")
def make_completed(self, request, queryset):
    app_name = self.model._meta.app_label
    queryset.update(status=self.model.Status.Completed)
    self.message_user(
        request,
        f"Selected items have been marked as Compelted in the {app_name} app.",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "display_user",
        "created_date",
    )
    list_filter = ("created_at", "status")
    search_fields = (
        "title",
        "description",
        "status",
        "user__first_name",
        "user__username",
        "user__last_name"
    )
    ordering = ("-updated_at", "title")
    date_hierarchy = "created_at"
    list_per_page = 20
    actions = (make_completed, )
    readonly_fields = ("user", "slug")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def display_user(self, obj):
        user_name = (
            obj.user.get_full_name() if obj.user.get_full_name() else "Admin"
        )
        url = reverse("admin:users_customuser_change", args=[obj.user.id])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url,
            user_name,
        )
        return format_html(link)

    display_user.short_description = "Müəllif"  # type: ignore[attr-defined]

  