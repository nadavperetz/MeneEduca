from django import forms

from .models import QuestionAnswered, QuestionnaireAnswered
from django.forms.models import inlineformset_factory


class QuestionnaireAnsweredForm(forms.ModelForm):
    class Meta:
        model = QuestionnaireAnswered


