from django import template
from groups.models import Group
from educational.models import Discipline
register = template.Library()


@register.simple_tag()
def disciplines(**kwargs):
    groups = Group.objects.filter(profiles=kwargs['profile'])
    list_of = Discipline.objects.filter(group=groups)
    print list_of
    return list_of

