from django.urls import path
from . import views

urlpatterns = [
    path('assignment/',views.Task.as_view()),
    path('assignment/<int:pk>', views.EachTask.as_view()),
    path('assignment/<int:pk>/submission/', views.TaskSubmission.as_view())
]