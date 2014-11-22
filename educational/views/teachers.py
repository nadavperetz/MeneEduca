from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render

from educational.models import Discipline


class DisciplineDetailView(DetailView):
    model = Discipline


class DisciplineUpdateView(UpdateView):
    model = Discipline
    template_name = 'educational/teacher/disicpline_update_view.html'
    fields = ['name', 'code', 'start_date', 'finish_date', 'teacher']




