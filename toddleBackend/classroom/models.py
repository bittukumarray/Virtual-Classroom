from django.db import models

from authService.models import *

# Create your models here.

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    publish_at = models.DateTimeField()
    deadline_at = models.DateTimeField()
    description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(UserProfile, related_name="teacher", on_delete=models.CASCADE)
    created_for = models.ManyToManyField(UserProfile, related_name="students")


