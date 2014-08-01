from django.contrib import admin
from survey.models import Survey, QuestionIpip
from survey.models import OneAnswerIpip, AnswersIpipCompleted


class QuestionInline(admin.StackedInline):
    model = QuestionIpip
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]


class OneAnswerIpipInline(admin.StackedInline):
    model = OneAnswerIpip


class AnswersIpipCompletedAdmin(admin.ModelAdmin):
    inlines = [OneAnswerIpipInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(AnswersIpipCompleted, AnswersIpipCompletedAdmin)

# Register your models here.
