from rest_framework import exceptions as rest_exceptions


def task_check_permission(task, user):
    if task.owner != user:
        raise rest_exceptions.PermissionDenied(
            "Unauthorised access to task")
