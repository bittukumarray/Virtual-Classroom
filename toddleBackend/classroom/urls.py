from django.urls import path
from . import views

urlpatterns = [
    path('task/',views.Task.as_view()),

]