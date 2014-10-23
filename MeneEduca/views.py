from django.shortcuts import render
from account.decorators import login_required


@login_required
def index(request):
    return render(request, 'site_base.html')