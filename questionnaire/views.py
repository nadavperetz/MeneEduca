# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404, redirect, render

from .models import QuestionnaireModel, QuestionnaireAnswered, QuestionModel, QuestionAnswered
from .forms import HorizRadioRenderer


class QuestionnaireListView(ListView):
    model = QuestionnaireModel
    template_name = 'questionnaire/questionnaire_list_view.html'


def questionnaire_redirect(request, pk):
    questionnaire = get_object_or_404(QuestionnaireModel, pk=pk)
    q = QuestionnaireAnswered.objects.filter(
        questionnaire=questionnaire,
        student=request.user.profile.student)
    if q:
        if q[0].finish:
            return redirect('questionnaire:detail', pk=pk)
    return redirect('questionnaire:answer', pk=pk)


class QuestionnaireDetailView(DetailView):
    model = QuestionnaireAnswered
    template_name = 'questionnaire/questionnaire_detail.html'

    def get_object(self, **kwargs):
        questionnaire_answered = QuestionnaireAnswered.objects.get(
            questionnaire__pk=self.kwargs['pk'],
            student__profile=self.request.user.profile)
        return questionnaire_answered


def questionnaire_create_view(request, pk):
    questionnaire_model = QuestionnaireModel.objects.get(pk=pk)

    """A query abaixo busca o objeto, se nao existe, eh criado. A query devolve uma  devolve uma tupla (objeto, bool)
       O booleano indica se foi criado (True) ou ele ja existe(False"""
    questionnaire = QuestionnaireAnswered.objects.get_or_create(
        questionnaire=questionnaire_model,
        student=request.user.profile.student)
    if questionnaire[1]:  # Se o questionario foi criado
        for question in questionnaire_model.questionmodel_set.all():
            question_answer = QuestionAnswered(question=question,
                                               questionnaire=questionnaire[0])
            question_answer.save()
    else:
        if questionnaire[0].finish:
            return redirect('questionnaire:detail', pk=questionnaire[0].pk)
    lista_perguntas = list(questionnaire[0].questionanswered_set.all())
    questionnaire_formset = inlineformset_factory(
        QuestionnaireAnswered, QuestionAnswered,
        extra=len(lista_perguntas),
        can_delete=False,
        fields=['answer'],
        widgets={'answer': forms.RadioSelect(renderer=HorizRadioRenderer)})

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
                lista_perguntas[i].delete()
            i += 1
        questionnaire[0].finish = True
        questionnaire[0].save()
        return HttpResponseRedirect(reverse(
            'questionnaire:detail', kwargs={'pk': questionnaire_model.pk}))
    else:
        formset = questionnaire_formset()
        for subform, question in zip(formset.forms, lista_perguntas):
            subform.instance.question = question.question
            subform.initial = {'question': question.question}
    context = {'questionnaire': questionnaire_model, 'formset': formset}
    return render(request, 'questionnaire/questionnaire_form.html', context)

