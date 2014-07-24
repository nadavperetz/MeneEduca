from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ["user",
                   "complete_profile",
                   "groups",
                   "created_at",
                   "modified_at"]

