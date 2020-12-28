from django.db import models
from django.contrib.auth import get_user_model


class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    header = models.CharField(max_length=255, null=False)
    description = models.TextField(default="", null=False)
    estimated_duration = models.DurationField(null=False)
    expiry_time = models.DateTimeField(null=False)
    is_completed = models.BooleanField(default=False, null=False)
