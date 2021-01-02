from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist

from .permissions import task_check_permission

from .models import Task
from datetime import datetime, timedelta

User = get_user_model()


def task_create(
    *,
    owner: User,
    header: str,
    description: str,
    estimated_duration: timedelta,
    expiry_time: datetime
) -> Task:
    task = Task(
        owner=owner,
        header=header,
        description=description,
        estimated_duration=estimated_duration,
        expiry_time=expiry_time,
        is_completed=False,
    )
    task.full_clean()
    task.save()

    return task


def task_update_for_user(
    *,
    task: Task,
    user: User,
    ** updated_fields: dict
) -> Task:
    task_check_permission(task, user)
    for field, value in updated_fields.items():
        if value is not None:
            setattr(task, field, value)
    task.full_clean()
    task.save()
    return task


def task_delete_for_user(
    *,
    task: Task,
    user: User
) -> Task:
    task_check_permission(task, user)
    task.delete()
    return task
