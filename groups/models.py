from django.db import models
from agora.models import Forum
from profiles.models import Profile
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=75, unique=True)
    profiles = models.ManyToManyField(Profile, blank=True, null=True)

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



