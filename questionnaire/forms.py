from django import forms

from .models import QuestionAnswered, QuestionnaireAnswered
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe

class QuestionnaireAnsweredForm(forms.ModelForm):
    class Meta:
        model = QuestionnaireAnswered


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))