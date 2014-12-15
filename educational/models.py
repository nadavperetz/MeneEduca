# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta
from django.utils import timezone
from groups.models import Group
from events_calendar.models import Event


class Discipline(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"name"))
    code = models.CharField(max_length=15, verbose_name=_(u"code"))
    start_date = models.DateField(verbose_name=_(u"Start date"),
                                  default=date(date.today().year, 1, 1))
    finish_date = models.DateField(verbose_name=_(u"Finish date"),
                                   default=date(date.today().year, 12, 31))
    teacher = models.ForeignKey('profiles.Teacher', related_name="discipline_of_teacher", verbose_name=_(u"teacher"))
    group = models.ForeignKey('groups.Group', blank=True, null=True, verbose_name=_(u"group"))
    parent_group  = models.ForeignKey('groups.Group', blank=True, null=True, verbose_name=_(u"group of parents"), related_name="group_of_parents")

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
            group = Group(name=self.name)
            group.save()
            group.profiles.add(self.teacher.profile)
            group.save()
            self.group = group

            parent_group = Group(name=u'{0} - {1}'.format(self.name, _(u'Guardians')))
            parent_group.save()
            parent_group.profiles.add(self.teacher.profile)
            parent_group.save()
            self.parent_group = parent_group
        self.group.name = self.name
        self.group.save()
        self.parent_group.name = u'{0} - {1}'.format(self.name, _(u'Guardians'))
        self.parent_group.save()
        super(Discipline, self).save()

    def __str__(self):
        return self.code + " " + self.name


"""
class Classroom(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"Name"))

    def __str__(self):
        return self.name


class Grade(models.Model):
    discipline = models.ForeignKey(Discipline)
    student = models.ForeignKey('profiles.Student', related_name="student_grade")
    value = models.FloatField(verbose_name=_(u"Value"))

    def __str__(self):
        text = str(self.student)[:10] + " " + str(self.student)[:10] + " "
        text += "[" + str(self.value) + "]"
        return text"""


class Assignment(models.Model):
    discipline = models.ForeignKey('educational.Discipline', verbose_name=_(u"discipline"))
    title = models.CharField(max_length=60, verbose_name=_(u"title"))
    group = models.ManyToManyField('groups.Group', blank=True, editable=False, verbose_name=_(u"group"))

    def __str__(self):
        opt = " Assign. "
        name = str(self.discipline.code) + opt
        name += str(self.title)
        return name

"""
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            group = Group(name=self.title)
            group.save()
            group.profiles.add(self.discipline.teacher.profile)
            group.save()
            self.group = group
        super(Assignment, self).save()
"""

class Deadline(models.Model):
    description = models.CharField(max_length=60, verbose_name=_(u"title"))
    start_date = models.DateTimeField(default=timezone.now(), verbose_name=_(u"start date"))
    finish_date = models.DateTimeField(verbose_name=_(u"finish date"))
    assignment = models.ForeignKey(Assignment, verbose_name=_(u"assignment"))
    event = models.ManyToManyField('events_calendar.Event', blank=True, null=True, verbose_name=_(u"eventos"))

    def __str__(self):
        text = str(self.description)
        return text

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            super(Deadline, self).save()
            for user in self.assignment.group.profiles.all():
                event = Event.objects.get_or_create(description=self.description,
                                                    start_date=self.start_date,
                                                    finish_date=self.finish_date,
                                                    profile=user)
                if event[1]:  # Se foi criado
                    self.event.add(event[0])  # Adicionar
        super(Deadline, self).save()


class Remainder(models.Model):
    start_date = models.DateField(default=timezone.now(), verbose_name=_(u"start date"))
    finish_date = models.DateField(verbose_name=_(u"finish date"))
    description = models.CharField(max_length=60, verbose_name=_(u"description"))
    forum = models.ForeignKey('agora.Forum', verbose_name=_(u"forum"))

