from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="profile",on_delete=models.CASCADE)
    role = models.CharField(default="student", max_length=10)
    def __str__(self):
        return str(self.user) +" - " + self.role
