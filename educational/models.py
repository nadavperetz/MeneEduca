from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date
from profiles.models import Teacher, Student
from groups.models import Group


class Discipline(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"name"))
    code = models.CharField(max_length=15, verbose_name=_(u"code"))
    start_date = models.DateField(verbose_name=_(u"Start date"),
                                  default=date(date.today().year, 1, 1))
    finish_date = models.DateField(verbose_name=_(u"Finish date"),
                                   default=date(date.today().year, 12, 31))
    teacher = models.ForeignKey(Teacher)
    group = models.ForeignKey('groups.Group')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.code:
            self.code = self.name[:15]
        super(Discipline, self).save()

    def __str__(self):
        return self.code + " " + self.name


class Classroom(models.Model):
    name = models.CharField(max_length=60, verbose_name=_(u"Name"))

    def __str__(self):
        return self.name


class Grade(models.Model):
    discipline = models.ForeignKey(Discipline)
    student = models.ForeignKey(Student)
    value = models.FloatField(verbose_name=_(u"Value"))

    def __str__(self):
        text = str(self.student)[:10] + " " + str(self.student)[:10] + " "
        text += "[" + str(self.value) + "]"
        return text


class Assignment(models.Model):
    discipline = models.ForeignKey('educational.Discipline')
    title = models.CharField(max_length=60, verbose_name=_(u"title"))
    group = models.ForeignKey('groups.Group', blank=True, editable=False)

    def __str__(self):
        opt = " Assign. "
        name = str(self.discipline.code) + opt
        name += str(self.title)
        return name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            group = Group(name='teste')
            self.group = group
        super(Assignment, self).save()
