from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.http import urlquote
from django.views.generic import ListView
from django.views.generic.base import TemplateView
#from .utils import send_mail_template

from .forms import FormForForm
from .models import Form
from .settings import USE_SITES, EMAIL_FAIL_SILENTLY
from .signals import form_invalid, form_valid
from .utils import split_choices


class SurveyListView(ListView):
    model = Form
    template_name = "survey/survey_list_view.html"


class SurveyCompletedListView(ListView):
    model = Form
    template_name = "survey/survey_completed_list_view.html"


class FormDetail(TemplateView):
    template_name = "survey/forms/form_detail.html"

    def get_context_data(self, **kwargs):
        context = super(FormDetail, self).get_context_data(**kwargs)
        published = Form.objects.published(for_user=self.request.user)
        context["form"] = get_object_or_404(published, slug=kwargs["slug"])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        login_required = context["form"].login_required
        if login_required and not request.user.is_authenticated():
            path = urlquote(request.get_full_path())
            bits = (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
            return redirect("%s?%s=%s" % bits)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        published = Form.objects.published(for_user=request.user)
        form = get_object_or_404(published, slug=kwargs["slug"])
        form_for_form = FormForForm(form, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None)
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            # Attachments read must occur before model save,
            # or seek() will fail on large uploads.
            attachments = []
            for f in form_for_form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
        context = {"form": form, "form_for_form": form_for_form}
        return self.render_to_response(context)

    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            json_context = json.dumps({
                "errors": context["form_for_form"].errors,
                "form": context["form_for_form"].as_p(),
                "message": context["form"].response,
            })
            return HttpResponse(json_context, content_type="application/json")
        return super(FormDetail, self).render_to_response(context, **kwargs)

form_detail = FormDetail.as_view()


def form_sent(request, slug, template="forms/form_sent.html"):
    """
    Show the response message.
    """
    published = Form.objects.published(for_user=request.user)
    context = {"form": get_object_or_404(published, slug=slug)}
    return render_to_response(template, context, RequestContext(request))
