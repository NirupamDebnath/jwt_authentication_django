from django.urls import include, path

from rest_framework import routers

from authentication import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('refresh/', views.RefreshTokenView.as_view()),
]
