from django.db import models
from profiles.models import Profile
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=75, unique=True)
    profiles = models.ManyToManyField(Profile, blank=True, null=True)

    def is_discipline(self):
        if self.discipline_set:
            return True
        else:
            return False

    def __str__(self):
        return self.name


