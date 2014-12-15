from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect

from educational.models import Assignment

class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'educational/guardian/assignment_detail.html'
