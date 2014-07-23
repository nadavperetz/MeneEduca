import os
import uuid

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)

class Groups(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=75, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    bio = models.TextField(blank=True)

    complete_profile = models.BooleanField(default=False)

    groups = models.ManyToManyField(Groups,
                                    default="General")


    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Profile, self).save(*args, **kwargs)




class Course(models.Model):
    course_name = models.CharField(max_length=75)


class Teacher(Profile):
    courses = models.ManyToManyField(Course,
                                     blank=True,
                                     null=True)
    def save(self, *args, **kwargs):
        try:
            group = Groups.objects.get(name="Teachers")
        except:
            group = Groups(name="Teachers")
            group.save()
        Profile.groups.add(group)
        Profile.save(update_fields=['groups'])


class Student(Profile):
    courses = models.ManyToManyField(Course,
                                     blank=True,
                                     null=True)
    def save(self, *args, **kwargs):
        try:
            group = Groups.objects.get(name="Students")
        except:
            group = Groups(name="Students")
            group.save()
        Profile.groups.add(group)
        Profile.save(update_fields=['groups'])


class Guardian(Profile):
    #a.k.a. Parent
    profile = models.OneToOneField(Student)
    def save(self, *args, **kwargs):
        try:
            group = Groups.objects.get(name="Guardians")
        except:
            group = Groups(name="Guardians")
            group.save()
        Profile.groups.add(group)
        Profile.save(update_fields=['groups'])
