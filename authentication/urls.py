from django.urls import include, path

from authentication import views

urlpatterns = [
    path('access/', views.LoginView.as_view()),
    path('refresh/', views.RefreshTokenView.as_view()),
]
