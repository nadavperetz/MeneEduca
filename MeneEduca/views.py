from django.shortcuts import render
from account.decorators import login_required
from educational.models import Discipline
from groups.models import Group


@login_required
def index(request):
    groups = Group.objects.filter(profiles=request.user.profile)
    disciplines = Discipline.objects.filter(group=groups)
    return render(request, 'index.html', {'disciplines' : disciplines})