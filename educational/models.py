# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta
from django.utils import timezone
from profiles.models import Teacher, Student
from groups.models import Group


class Discipline(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"name"))
    code = models.CharField(max_length=15, verbose_name=_(u"code"))
    start_date = models.DateField(verbose_name=_(u"Start date"),
                                  default=date(date.today().year, 1, 1))
    finish_date = models.DateField(verbose_name=_(u"Finish date"),
                                   default=date(date.today().year, 12, 31))
    teacher = models.ForeignKey(Teacher, related_name="discipline_of_teacher")
    group = models.ForeignKey('groups.Group', blank=True, null=True)

    def is_active(self):
        if date.today() > self.finish_date:
            return False
        else:
            return True

    def get_next_assignments(self, delta=7):
        end = timezone.now() + timedelta(days=delta)
        assignments = Assignment.objects.filter(discipline=self)
        deadlines = []
        for assig in assignments:
            filtered = assig.deadlines.filter(finish_date__gte=end)
            deadlines.append(filtered)
        deadlines.sort()
        return deadlines

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            if not self.code:
                self.code = self.name[:15]
            group_teste = Group(name=str(self.name))
            group_teste.add(self.teacher)
            group_teste.save()
            self.group = group_teste
        super(Discipline, self).save()

    def __str__(self):
        return self.code + " " + self.name


class Classroom(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"Name"))

    def __str__(self):
        return self.name


class Grade(models.Model):
    discipline = models.ForeignKey(Discipline)
    student = models.ForeignKey(Student, related_name="student_grade")
    value = models.FloatField(verbose_name=_(u"Value"))

    def __str__(self):
        text = str(self.student)[:10] + " " + str(self.student)[:10] + " "
        text += "[" + str(self.value) + "]"
        return text


class Deadline(models.Model):
    description = models.CharField(max_length=60, verbose_name=_(u"title"))
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    def __str__(self):
        text = str(self.description)[10]
        return text


class Assignment(models.Model):
    discipline = models.ForeignKey('educational.Discipline')
    title = models.CharField(max_length=60, verbose_name=_(u"title"))
    group = models.ForeignKey('groups.Group', blank=True, editable=False)
    deadlines = models.ManyToManyField(Deadline, blank=True, null=True)

    def __str__(self):
        opt = " Assign. "
        name = str(self.discipline.code) + opt
        name += str(self.title)
        return name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            group = Group(name=self.title)
            group.add(self.discipline.teacher)
            group.save()
            self.group = group
        super(Assignment, self).save()
