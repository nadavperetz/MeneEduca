from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render

from educational.models import Discipline, Assignment

from fb.models import Likes

class DisciplineDetailView(DetailView):
    model = Discipline
    template_name = 'educational/teacher/discipline_detail.html'


class DisciplineUpdateView(UpdateView):
    model = Discipline
    template_name = 'educational/teacher/disicpline_update_view.html'
    fields = ['name', 'code', 'start_date', 'finish_date', 'teacher']

    def get_success_url(self):
        return reverse('educational:discipline_detail', kwargs={'pk': self.object.pk})


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'educational/teacher/assignment_detail.html'


class AssignmentCreateView(CreateView):
    model = Assignment
    template_name = 'educational/teacher/assignment_create_view.html'
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(AssignmentCreateView, self).get_context_data(**kwargs)
        context['discipline'] = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        return context

    def form_valid(self, form):
        form.instance.discipline = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        return super(AssignmentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('educational:discipline_detail', kwargs={'pk': self.kwargs['discipline_id']})


def assignment_create(request, discipline_id):
    discipline = get_object_or_404(Discipline, pk=discipline_id)
    return render(request, 'educational/teacher/assignment_create.html', {'discipline': discipline})

def social_network(request, discipline_id):
    discipline=Discipline.objects.get(pk=discipline_id)
    users=discipline.group.profiles.all()
    likes=Likes.objects.filter(profile__in=users)
    return render(request, 'educational/teacher/likes.html',{'likes' : likes})
    

