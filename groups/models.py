from django.db import models
from profiles.models import Profile
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=75)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name

