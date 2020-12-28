from django.urls import path, include

from .views import (
    TaskCreateApi
)

todo_patterns = [
    path('create/', TaskCreateApi.as_view(), name='create'),
]

app_name = 'todo'

urlpatterns = [
    path('tasks/', include((todo_patterns, 'tasks')))
]
