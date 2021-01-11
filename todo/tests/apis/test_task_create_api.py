from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import serializers, status


class TaskCreateApiTests(TestCase):
    class InputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, allow_blank=False)
        description = serializers.CharField(allow_blank=True)
        estimated_duration = serializers.DurationField(required=True)
        expiry_time = serializers.DateTimeField(required=True)

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('todo:tasks:create')

        self.user = get_user_model().objects.create_user(
            "test_user"
            "test@testmail.com",
            "testpass"
        )

        self.data = {
            'header': 'Some Task',
            'description': 'Some Task Description',
            'estimated_duration': 120,
            'expiry_time': '2021-01-11T00:00:06'
        }

        return super().setUp()

    @patch("todo.views.task_create")
    def test_view_calls_task_create(self, task_create_mock):
        """Test that views calls task_create service"""

        self.client.force_authenticate(self.user)

        serializer = self.InputSerializer(data=self.data)
        serializer.is_valid()
        task_create_mock.return_value = serializer.validated_data

        self.client.post(self.url, self.data)

        task_create_mock.assert_called_once_with(
            owner=self.user, **serializer.validated_data)

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.post(self.url, self.data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
