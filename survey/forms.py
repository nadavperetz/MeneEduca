# -*- coding: utf-8 -*-

from django import forms

from survey.models import OneAnswerIpip


class FormAnswerIpip(forms.ModelForm):
    class Meta:
        model = OneAnswerIpip
        exclude = ['question', 'all_answers']
