from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect

from educational.models import Discipline, Assignment
from groups.models import Group
from profiles.models import Profile


from educational.forms import GroupForm


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


class GroupListView(ListView):
    model = Group
    template_name = 'educational/teacher/group_list.html'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['assignment'] = Assignment.objects.get(pk=self.kwargs['assignment_id'])
        return context


class GroupDetailView(DetailView):
    model = Group
    template_name = 'educational/teacher/group_detail.html'


def group_update(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    assignment = Assignment.objects.filter(group=group)[0]

    # students = assignment.discipline.group.profiles.filter(student=True)
    students = []
    for profile in assignment.discipline.group.profiles.all():
        if profile.is_student():
            students.append(profile)

    if request.method == 'POST':
        form = GroupForm(students, request.POST)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            group.save()

            for profile in group.profiles.all():
                group.profiles.remove(profile)

            for selected_student in form.cleaned_data['students']:
                group.profiles.add(Profile.objects.get(pk=selected_student))
            group.profiles.add(assignment.discipline.teacher.profile)

            return HttpResponseRedirect(reverse("educational:assignment_detail", kwargs={'pk': assignment.pk}))
    else:
        old_students = []
        for profile in group.profiles.all():
            if profile.is_student():
                old_students.append(profile)
        print [s.pk for s in old_students]
        form = GroupForm(students, initial={'name': group.name, 'students': [s.pk for s in old_students]})

    return render(request, 'educational/teacher/group_update.html', {'form': form})



def group_create(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # students = assignment.discipline.group.profiles.filter(student=True)
    students = []
    for profile in assignment.discipline.group.profiles.all():
        if profile.is_student():
            students.append(profile)

    if request.method == 'POST':
        form = GroupForm(students, request.POST)
        if form.is_valid():
            g = Group()
            g.name = form.cleaned_data['name']
            g.save()

            for selected_student in form.cleaned_data['students']:
                g.profiles.add(Profile.objects.get(pk=selected_student))
            g.profiles.add(assignment.discipline.teacher.profile)

            assignment.group.add(g)
            return HttpResponseRedirect(reverse("educational:assignment_detail", kwargs={'pk': assignment.pk}))

    else:
        form = GroupForm(students)

    return render(request, 'educational/teacher/group_create.html', {'form': form})
