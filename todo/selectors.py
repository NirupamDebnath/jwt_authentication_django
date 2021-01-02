from django.contrib.auth import get_user_model

import django_filters
from rest_framework import fields

from .models import Task
from .permissions import task_check_permission

User = get_user_model()


def task_get_by_id(id: int) -> Task:
    return Task.objects.get(pk=id)


def task_get(task_id: int, user: User) -> Task:
    task = task_get_by_id(task_id)
    task_check_permission(task, user)
    return task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ("id", "header", "description",
                  "estimated_duration", "expiry_time", "is_completed")


def task_list_for_user(*, user: User, filters: dict = None):
    filters = filters or {}
    qs = Task.objects.filter(owner=user)

    return TaskFilter(filters, qs).qs
