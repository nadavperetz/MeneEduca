from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    description = models.CharField(max_length=60, verbose_name=_(u"title"))
    start_date = models.DateTimeField(default=timezone.now())
    finish_date = models.DateTimeField()
    profile = models.ForeignKey('profiles.Profile')

    def __str__(self):
        text = str(self.description)[:10]
        return text

    class Meta:
        ordering = ['finish_date', 'start_date']