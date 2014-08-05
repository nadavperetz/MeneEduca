# coding=utf-8
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from survey.models import Survey, QuestionIpip, AnswersIpipCompleted, OneAnswerIpip
from survey.forms import FormAnswerIpip


@login_required
def index(request):
    return render(request, "survey/index.html")


@login_required
def survey_ipip(request, survey_id):
    this_survey = get_object_or_404(Survey, pk=survey_id)
    answer_ipip_completed, created = AnswersIpipCompleted.objects.get_or_create(
        profile=request.user.profile,
        survey=this_survey)
    if not answer_ipip_completed.completed:
        questions = get_list_or_404(QuestionIpip, survey=this_survey)
        extra = (len(questions))
        form_ipip_formset = formset_factory(FormAnswerIpip, extra=extra)
        mylist = []
        if request.method == 'POST':
            """Ainda esta incompleto!!!!
               Esta solucao nao é dentro dos padroes do django!!!!!!!!!!!!!!!!!
                """
            formset = form_ipip_formset(request.POST)
            for form in formset.data.iteritems():
                if form[0][6:] == "-answer_value":
                    number = int(form[0][5])
                    one_answer = OneAnswerIpip(question=questions[number],
                                               all_answers=answer_ipip_completed,
                                               answer_value=int(form[1]),
                                               )
                    one_answer.save()
            answer_ipip_completed.completed = True
            answer_ipip_completed.save()
            return HttpResponseRedirect(reverse('survey:survey_result', args=(survey_id, )))
        else:
            formset = form_ipip_formset()
            for subform, question in zip(formset.forms, questions):
                mylist.append([subform, question])
        context = {'formset': formset, 'survey': this_survey,
                   'questions': questions, 'mylist': mylist}
        return render(request, "survey/questions.html", context)
    else:
        return HttpResponseRedirect(reverse('survey:survey_result', args=(survey_id, )))


def survey_result(request, survey_id):
    this_survey = get_object_or_404(Survey, pk=survey_id)
    answer_ipip_completed = AnswersIpipCompleted.objects.filter(profile=request.user.profile,
                                                             survey=this_survey)

    if answer_ipip_completed:
        answer_ipip_completed = answer_ipip_completed[0]
        if answer_ipip_completed.completed:
            questions = get_list_or_404(OneAnswerIpip, all_answers=answer_ipip_completed)
            context = {'survey': this_survey,'questions': questions}
            return render(request, "survey/survey.html", context)
        else:
            return HttpResponseRedirect(reverse('survey:survey_ipip', args=(survey_id, )))
    else:
        return HttpResponseRedirect(reverse('survey:survey_ipip', args=(survey_id, )))