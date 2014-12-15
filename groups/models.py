# -*- encoding: utf-8 -*-
from django.db import models
from agora.models import Forum
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=75, unique=False)
    profiles = models.ManyToManyField("profiles.Profile", blank=True, null=True)

    def is_discipline(self):
        if self.discipline_set.all():
            return True
        else:
            return False

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            super(Group, self).save()
            description = "Forum " + str(self.name)
            forum = Forum(title=self.name,
                          description=description,
                          group=self)
            forum.save()
        else:
            super(Group, self).save()
