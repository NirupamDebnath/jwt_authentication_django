from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import serializers, status

from ...models import Task


class TaskListApiTests(TestCase):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        header = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        estimated_duration = serializers.DurationField(required=False)
        expiry_time = serializers.DateTimeField(required=False)
        is_completed = serializers.BooleanField(required=False)

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('todo:tasks:list')

        self.user = get_user_model().objects.create_user(
            "test_user"
            "test@testmail.com",
            "testpass"
        )

        self.filter_data = {
            'header': 'Some Task',
            'description': 'Some Task Description',
            'estimated_duration': 120,
            'expiry_time': '2021-01-11T00:00:06',
            'is_completed': True,
        }

        return super().setUp()

    @patch("todo.views.task_list_for_user")
    def test_view_calls_task_list_for_user(self, task_list_for_user_mock):
        """Test that views calls task_update_for_user service"""

        self.client.force_authenticate(self.user)

        task_list_for_user_mock.return_value = Task.objects.all()
        filter_serializer = self.FilterSerializer(data=self.filter_data)
        filter_serializer.is_valid(raise_exception=True)

        self.client.get(self.url, self.filter_data)

        task_list_for_user_mock.assert_called_once_with(
            user=self.user, filters=filter_serializer.validated_data)

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.post(self.url, self.filter_data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
