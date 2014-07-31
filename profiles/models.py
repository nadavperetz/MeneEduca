import os
import uuid

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)

class Group(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    bio = models.TextField(blank=True)

    complete_profile = models.BooleanField(default=False)

    group = models.ManyToManyField(Group,
                                    default="General")


    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def is_student(self):
        if Student.objects.get(pk = self.id):
            return True
        else:
            return False

    def is_teacher(self):
        if Teacher.objects.get(pk = self.id):
            return True
        else:
            return False

    def is_guardian(self):
        if Guardian.objects.get(pk = self.id):
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        if not self.Group.all():
            self.Group.add(Group.objects.get(name="General"))
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.name, self.last_name)



class Course(models.Model):
    course_name = models.CharField(max_length=75)

    def __str__(self):
        return self.course_name

class Teacher(Profile):
    courses = models.ManyToManyField(Course,
                                     blank=True,
                                     null=True)
    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Teacher, self).save(*args, **kwargs)
        if not self.Group.all():
            self.Group.add(Group.objects.get(name="General"))
            self.Group.add(Group.objects.get(name="Teachers"))


class Student(Profile):
    courses = models.ManyToManyField(Course,
                                     blank=True,
                                     null=True)
    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Student, self).save(*args, **kwargs)
        if not self.Group.all():
            self.Group.add(Group.objects.get(name="General"))
            self.Group.add(Group.objects.get(name="Students"))


class Guardian(Profile):
    #a.k.a. Parent
    profile = models.ForeignKey(Student)
    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Guardian, self).save(*args, **kwargs)
        if not self.Group.all():
            self.Group.add(Group.objects.get(name="General"))
            self.Group.add(Group.objects.get(name="Guardians"))