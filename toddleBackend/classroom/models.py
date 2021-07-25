from django.db import models

from authService.models import *
from django.utils import timezone
# Create your models here.

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    publish_at = models.DateTimeField()
    deadline_at = models.DateTimeField()
    description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(UserProfile, related_name="teacher", on_delete=models.CASCADE)
    created_for = models.ManyToManyField(UserProfile, related_name="students")

    def __str__(self):
        return "by " + str(self.created_by)


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=2000)

    class Meta:
        unique_together = ('assignment', 'user',)

    def __str__(self):
        return "by " + str(self.user)