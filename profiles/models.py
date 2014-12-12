import os
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from educational.models import Discipline

# for personality traits
import random


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    print os.path.join("avatars", filename)
    return os.path.join("avatars", filename)


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True, default='avatars/default.jpg')
    bio = models.TextField(blank=True)
    complete_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def is_student(self):
        try:
            Student.objects.get(profile=self)
        except Student.DoesNotExist:
            return False
        return True

    def is_teacher(self):
        try:
            Teacher.objects.get(profile=self)
        except Teacher.DoesNotExist:
            return False
        return True

    def is_guardian(self):
        try:
            Guardian.objects.get(profile=self)
        except Guardian.DoesNotExist:
            return False
        return True

    def discipline_and_groups(self):
        returning = {}
        if self.is_student():
            disciplines = Discipline.objects.filter(group__profiles=self)
            # print disciplines
            for discipline in disciplines:
                aux = []
                assignments = discipline.assignment_set.all()
                for assign in assignments:
                    # print assign
                    group = assign.group.filter(profiles=self)
                    if group:
                        aux.append(group.first())
                # print aux
                returning[discipline.group] = aux
            # print returning
        return returning


    def __str__(self):
        return "%s %s" % (self.name, self.last_name)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Profile, self).save(*args, **kwargs)

    # to-do
    def get_traits(self):
        traits = []
        for x in range(5):
            traits.append(random.uniform(0, 1))
        return traits


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
    children = models.ManyToManyField(Student, related_name='guardians_children')

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()

    def __str__(self):
        return "%s %s" % (self.profile.name, self.profile.last_name)
