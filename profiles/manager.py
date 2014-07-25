def verifyFullProfile(request_user):
    if request_user.is_authenticated():
        return request_user.profile.complete_profile
    else:
        return False

