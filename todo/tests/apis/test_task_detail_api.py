from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import serializers

from ...models import Task


class TaskDetailApiTests(TestCase):
    class OutputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        estimated_duration = serializers.DurationField(required=False)
        expiry_time = serializers.DateTimeField(required=False)
        is_completed = serializers.BooleanField(required=False)

    def setUp(self) -> None:
        self.client = APIClient()
        self.task_id = 1
        self.url = reverse('todo:tasks:detail', args=(self.task_id,))

        self.user = get_user_model().objects.create_user(
            "test_user"
            "test@testmail.com",
            "testpass"
        )

        self.data = {
            'header': 'Some Task',
            'description': 'Some Task Description',
            'estimated_duration': 120,
            'expiry_time': '2021-01-11T00:00:06',
            'is_completed': True,
        }

        return super().setUp()

    @patch("todo.views.task_get_for_user")
    def test_view_calls_task_get_for_user(self, task_get_for_user_mock):
        """Test that views calls task_update_for_user service"""

        self.client.force_authenticate(self.user)

        serializer = self.OutputSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        task_get_for_user_mock.return_value = Task(**serializer.validated_data)

        self.client.get(self.url)

        task_get_for_user_mock.assert_called_once_with(
            task_id=self.task_id, user=self.user)
