from django import forms
from django.utils.translation import ugettext_lazy as _

class GroupForm(forms.Form):
    def __init__(self, profiles, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label=_(u'Name'), max_length=100)
        self.fields['students'] = forms.MultipleChoiceField(label=_(u'Students'), choices=[(p.pk, p) for p in profiles])
        self.fields['students'].help_text = _('Hold down "Control", or "Command" on a Mac, to select more than one.')

class PersonalityBasedGroupForm(forms.Form):
    def __init__(self, max_groups, *args, **kwargs):
        super(PersonalityBasedGroupForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(label=_(u'Name'), max_length=100)
        self.fields['name'].help_text = _('Name base of the groups. A number to identify the different groups will be appended to this name.')
        self.fields['number'] = forms.IntegerField(label=_(u'Number of groups'), min_value=1, max_value=max_groups)
        self.fields['number'].help_text = _('The number of groups that will be generated. This must be less than or equal to the number of students enrolled in the discipline.')
        self.fields['algorithm'] = forms.ChoiceField(label=_(u'Algorithm'), choices=[(1, 'Bruteforce'), (2, 'Random best'), (3, 'Random')])
        self.fields['algorithm'].help_text = _("The bruteforce algorithm tries all the possible group formations. It should not be used when there's a big number of students. Random best chooses the best group formation after 1 second of random tries. Random generates a random group.")
