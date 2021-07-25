from django.urls import path
from . import views

urlpatterns = [
    path('task/',views.Task.as_view()),
    path('task/<int:pk>', views.EachTask.as_view())

]