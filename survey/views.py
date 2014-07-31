from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponse

from survey.models import Survey, QuestionIpip
from survey.forms import FormAnswerIpip

# Create your views here.


def survey_ipip(request, survey_id):
    this_survey = get_object_or_404(Survey, pk=survey_id)
    questions = get_list_or_404(QuestionIpip, survey=this_survey)
    extra = (len(questions) - 1)
    form_ipip_formset = formset_factory(FormAnswerIpip, extra=extra)
    if request.method == 'POST':
        formset = form_ipip_formset(request.POST)
        if formset.is_valid:
            for form in formset:
                form.save()
                return reverse('survey_result')
    else:
        formset = form_ipip_formset()
        print formset
    context = {'formset': formset, 'survey': this_survey,
               'questions': questions}
    return render(request, "survey/questions.html", context)


def survey_result(request):
    return HttpResponse("Hello World")