from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404, redirect

from .models import QuestionnaireModel, QuestionnaireAnswered
from .forms import QuestionnaireForm


class QuestionnaireListView(ListView):
    model = QuestionnaireModel
    template_name = 'questionnaire/questionnaire_list_view.html'


def questionnaire_redirect(request, pk):
    questionnaire = get_object_or_404(QuestionnaireModel, pk=pk)
    questionnaire_answered = QuestionnaireAnswered.objects.filter(
        questionnaire=questionnaire,
        student=request.user.profile)
    if questionnaire_answered:
        return redirect('questionnaire:detail', pk=pk)
    else:
        return redirect('questionnaire:answer', pk=pk)


class QuestionnaireDetailView(DetailView):
    model = QuestionnaireAnswered
    template_name = 'questionnaire/questionnaire_detail.html'

    def get_object(self, **kwargs):
        print 'oi'
        questionnaire_answered = QuestionnaireAnswered.objects.get(
            questionnaire__pk=self.kwargs['pk'],
            student=self.request.user.profile)
        print questionnaire_answered
        return questionnaire_answered


class QuestionnaireCreateView(CreateView):
    form_class = QuestionnaireForm
    template_name = 'questionnaire/questionnaire_form.html'