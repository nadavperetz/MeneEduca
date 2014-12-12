from django import forms
from django.utils.translation import ugettext_lazy as _

class NameForm(forms.Form):
    def __init__(self, profiles, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label=_(u'Name'), max_length=100)
        self.fields['students'] = forms.MultipleChoiceField(label=_(u'Students'), choices=[(p.pk, p) for p in profiles])
