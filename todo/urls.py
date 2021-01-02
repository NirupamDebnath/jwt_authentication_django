from django.urls import path, include

from .views import (
    TaskListApi,
    TaskDetailApi,
    TaskCreateApi,
    TaskUpdateApi,
    TaskDeleteApi,
)

todo_patterns = [
    path('', TaskListApi.as_view(), name='list'),
    path('<int:task_id>/', TaskDetailApi.as_view(), name='detail'),
    path('create/', TaskCreateApi.as_view(), name='create'),
    path('<int:task_id>/update/', TaskUpdateApi.as_view(), name='update'),
    path('<int:task_id>/delete/', TaskDeleteApi.as_view(), name='delete'),
]

app_name = 'todo'

urlpatterns = [
    path('tasks/', include((todo_patterns, 'tasks')))
]
