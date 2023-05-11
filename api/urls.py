from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('list', views.TaskListView.as_view(), name='task_lists'),
    path('list/<uuid:uuid>', views.TaskListDetailsView.as_view(), name='task_list_details'),
    path('task', views.TaskView.as_view(), name='tasks'),
    path('task/<uuid:uuid>', views.TaskDetailsView.as_view(), name='task_details'),
]
