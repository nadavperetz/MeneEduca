from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404, redirect, render

from .models import QuestionnaireModel, QuestionnaireAnswered, QuestionModel, QuestionAnswered


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
        questionnaire_answered = QuestionnaireAnswered.objects.get(
            questionnaire__pk=self.kwargs['pk'],
            student=self.request.user.profile)
        return questionnaire_answered


def questionnaire_create_view(request, pk):
    questionnaire_model = QuestionnaireModel.objects.get(pk=pk)
    questionnaire = QuestionnaireAnswered.objects.get_or_create(
        questionnaire=questionnaire_model,
        student=request.user.profile.student)
    """"
    if questionnaire[1]:  # Se o questionario foi criado
        for question in questionnaire_model.questionmodel_set.all():
            question_answer = QuestionAnswered(question=question,
                                               questionnaire=questionnaire[0])
            question_answer.save()"""

    lista_perguntas = list(questionnaire[0].questionanswered_set.all())
    questionnaire_formset = inlineformset_factory(
        QuestionnaireAnswered, QuestionAnswered,
        extra=len(lista_perguntas),
        can_delete=False,
        fields=['answer'])

    if request.method == 'POST':
        formset = questionnaire_formset(request.POST)
        i = 0
        for form in formset.forms:
            if form.is_valid():
                form.cleaned_data['questionnaire'] = questionnaire[0]
                teste = form.save(commit=False)
                teste.answered = True
                teste.question = lista_perguntas[i].question
                teste.questionnaire = questionnaire[0]
                teste.save()
            i += 1
        return reverse('questionnaire:detail')
    else:
        formset = questionnaire_formset()
        for subform, question in zip(formset.forms, lista_perguntas):
            subform.instance.question = question.question
            print subform.initial
            subform.initial = {'question': question.question}
            print subform.initial
    context = {'questionnaire': questionnaire_model, 'formset': formset}
    return render(request, 'questionnaire/questionnaire_form.html', context)

