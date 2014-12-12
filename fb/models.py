from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
# Create your models here.

   
class Likes(models.Model):
    profile=models.ForeignKey(Profile)
    category=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    def __unicode__(self):
       return self.name
    class Meta:
        verbose_name = 'Likes'
        verbose_name_plural = "Likes"
        
        