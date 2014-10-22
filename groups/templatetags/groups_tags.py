from django import template
from groups.models import Group
register = template.Library()

@register.simple_tag()
def disciplines(profile):
    groups = Group.objects.filter(profiles=profile,
                                  is_discipline=True)
    return groups


