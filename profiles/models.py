import os
import uuid

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    bio = models.TextField(blank=True)
    complete_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def is_student(self):
        if Student.objects.get(profile=self):
            return True
        else:
            return False

    def is_teacher(self):
        if Teacher.objects.get(profile=self):
            return True
        else:
            return False

    def is_guardian(self):
        if Guardian.objects.get(profile=self):
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.name, self.last_name)


class Course(models.Model):
    course_name = models.CharField(max_length=75)

    def __str__(self):
        return self.course_name


class Teacher(models.Model):
    profile = models.OneToOneField(Profile)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.profile.name, self.profile.last_name)


class Student(models.Model):
    profile = models.OneToOneField(Profile)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.profile.name, self.profile.last_name)


class Guardian(models.Model):
    # a.k.a. Parent
    profile = models.OneToOneField(Profile)
    children = models.ManyToManyField(Student,
                                      related_name='guardians_children')

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()

    def __str__(self):
        return "%s %s" % (self.profile.name, self.profile.last_name)