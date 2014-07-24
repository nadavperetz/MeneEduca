from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile

class ProfileEditView(UpdateView):
    form_class = ProfileForm
    model = Profile


    def get_object(self):
        user = self.request.user.profile
        return user

    def get_success_url(self):
        return reverse("profiles_edit")

    def form_valid(self, form):
        response = super(ProfileEditView, self).form_valid(form)
        messages.success(self.request, "You successfully updated your profile.")
        return response
