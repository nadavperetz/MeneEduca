from django.contrib import admin
from .models import QuestionModel, QuestionnaireModel, QuestionnaireAnswered, QuestionAnswered


class QuestionInLine(admin.StackedInline):
    model = QuestionModel
    extra = 4


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine]


class QuestionnaireAnsweredAdmin(admin.ModelAdmin):
    fields = ('questionnaire', 'values')


admin.site.register(QuestionnaireModel, QuestionnaireAdmin)
admin.site.register(QuestionnaireAnswered, QuestionnaireAnsweredAdmin)
admin.site.register(QuestionAnswered)

