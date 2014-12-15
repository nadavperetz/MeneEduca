# -*- encoding: utf-8 -*-
from django.db import models
from agora.models import Forum
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
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
        super(Group, self).save()
        print self.name
        description = "Forum " + unicode(self.name)

        if not self.pk:
            forum = Forum(title=self.name,
                          description=description,
                          group=self)
            forum.save()
        else:
            forum = Forum.objects.filter(group=self)[0]
            forum.title = self.name
            forum.description = description
            forum.save()
