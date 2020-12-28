from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from common.utils import ApiErrorsMixin

from .services import task_create


class TaskCreateApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        header = serializers.CharField(max_length=255, allow_blank=False)
        description = serializers.CharField(allow_blank=True)
        estimated_duration = serializers.DurationField(required=True)
        expiry_time = serializers.DateTimeField(required=True)

    # used for browsable api only
    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_create(user=request.user, **serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
