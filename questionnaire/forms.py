from django import forms

from profiles.models import Profile


class QuestionnaireForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ["user",
                   "complete_profile",
                   "created_at",
                   "modified_at",
                   "group"]

