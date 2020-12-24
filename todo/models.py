from django.db import models
from django.contrib.auth import get_user_model


class TODO(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task_header = models.CharField(max_length=255, null=False)
    is_completed = models.BooleanField(default=False, null=False)
