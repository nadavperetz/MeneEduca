from django.shortcuts import redirect
from forums.profiles.models import Profile

def verifyFullProfile(request_user):
    if request_user.is_authenticated():
        return request_user.profile.complete_profile
    else:
        return False

