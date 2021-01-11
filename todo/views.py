from todo.models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from common.utils import ApiErrorsMixin

from .services import (task_create, task_update_for_user, task_delete_for_user)
from .selectors import task_get_by_id, task_get_for_user, task_list_for_user
from .pagination import get_paginated_response, LimitOffsetPagination


class TaskCreateApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, allow_blank=False)
        description = serializers.CharField(allow_blank=True)
        estimated_duration = serializers.DurationField(required=True)
        expiry_time = serializers.DateTimeField(required=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ("id", "header", "description", "estimated_duration",
                      "expiry_time", "is_completed")

    # used for browsable api only
    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = task_create(owner=request.user, **serializer.validated_data)
        serializer = self.OutputSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskUpdateApi(ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        estimated_duration = serializers.DurationField(required=False)
        expiry_time = serializers.DateTimeField(required=False)
        is_completed = serializers.BooleanField(required=False)

    # used for browsable api only
    serializer_class = InputSerializer

    def post(self, request, task_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = task_get_by_id(task_id)
        task_update_for_user(task=task, user=request.user,
                             **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class TaskDetailApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ("id", "header", "description", "estimated_duration",
                      "expiry_time", "is_completed")

    def get(self, request, task_id):
        task = task_get_for_user(task_id=task_id, user=request.user)
        serializer = self.OutputSerializer(task)

        return Response(serializer.data)


class TaskListApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        header = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        estimated_duration = serializers.DurationField(required=False)
        expiry_time = serializers.DateTimeField(required=False)
        is_completed = serializers.BooleanField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ("id", "header", "description", "estimated_duration",
                      "expiry_time", "is_completed")

    def get(self, request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        tasks = task_list_for_user(
            user=request.user, filters=filter_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=tasks,
            request=request,
            view=self
        )


class TaskDeleteApi(ApiErrorsMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = ("header", "description", "estimated_duration",
                      "expiry_time", "is_completed")

    def delete(self, request, task_id):
        task = task_get_by_id(task_id)
        task = task_delete_for_user(task=task, user=request.user)
        serializer = self.OutputSerializer(task)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
