from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from django.contrib import messages

from forms import ProfileForm
from profiles.models import Profile
from account.models import EmailAddress


class ProfileEditView(UpdateView):
    form_class = ProfileForm
    model = Profile

    def get_object(self, **kwargs):
        user = self.request.user.profile
        return user

    def get_success_url(self):
        return reverse("profiles:profiles_edit")

    """def post(self, request, *args, **kwargs):

        return super(ProfileEditView, self).post(request, *args, **kwargs)"""

    def form_valid(self, form):
        response = super(ProfileEditView, self).form_valid(form)
        email = EmailAddress.objects.get(user = self.request.user)
        profile = Profile.objects.get(user = self.request.user)
        if not email.verified:
            messages.warning(self.request, "You need to authenticate your email address in order to navigate \
                                           through the site")
        else:
            if not profile.complete_profile:
                profile.complete_profile = True
                profile.save()
            messages.success(self.request, "You successfully updated your profile.")
        return response
