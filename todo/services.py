from django.contrib.auth import get_user_model

from .models import Task
from datetime import datetime, timedelta

User = get_user_model()


def task_create(
    *,
    user: User,
    header: str,
    description: str,
    estimated_duration: timedelta,
    expiry_time: datetime
) -> Task:
    task = Task(
        user=user,
        header=header,
        description=description,
        estimated_duration=estimated_duration,
        expiry_time=expiry_time,
        is_completed=False,
    )
    task.full_clean()
    task.save()

    return task
