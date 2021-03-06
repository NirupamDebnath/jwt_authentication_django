from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import serializers


class TaskUpdateApiTests(TestCase):
    class OutputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        estimated_duration = serializers.DurationField(required=False)
        expiry_time = serializers.DateTimeField(required=False)
        is_completed = serializers.BooleanField(required=False)

    def setUp(self) -> None:
        self.client = APIClient()
        self.task_id = 1
        self.url = reverse('todo:tasks:update', args=(self.task_id,))

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

    @patch("todo.views.task_get_by_id")
    @patch("todo.views.task_update_for_user")
    def test_view_calls_task_update_for_user(self, task_update_for_user_mock, task_get_by_id_mock):
        """Test that views calls task_update_for_user service"""

        self.client.force_authenticate(self.user)
        task_get_by_id_mock.return_value = self.task_id

        self.client.post(self.url, self.data)

        serializer = self.OutputSerializer(data=self.data)
        serializer.is_valid()

        task_get_by_id_mock.assert_called_once_with(self.task_id)
        task_update_for_user_mock.assert_called_once_with(task=self.task_id,
                                                          user=self.user, **serializer.validated_data)
