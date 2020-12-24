from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from authentication.utils import get_token_pair_for_user, refresh_token_pair

import logging
logger = logging.getLogger(__name__)


class LoginView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username', 'email', 'first_name', 'last_name')

    # used for browsable api only
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(
            style={'input_type': 'password', 'placeholder': 'Password'})

    # used for browsable api only
    serializer_class = InputSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user:
            access, refresh = get_token_pair_for_user(user)
            serializer = self.OutputSerializer(user)
            data = {"user": serializer.data,
                    "access": access, "refresh": refresh}

            return Response(data, status=status.HTTP_200_OK)

        return Response({"detail": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    # used for browsable api only
    class InputSerializer(serializers.Serializer):
        refresh = serializers.CharField()

    # used for browsable api only
    serializer_class = InputSerializer

    def post(self, request):
        data = request.data
        refresh_token = data.get('refresh', '')
        access, refresh = refresh_token_pair(refresh_token=refresh_token)

        return Response({'access': access, 'refresh': refresh})
