from django.contrib import admin
from .models import QuestionModel, QuestionnaireModel


class QuestionInLine(admin.StackedInline):
    model = QuestionModel
    extra = 4


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine]


admin.site.register(QuestionnaireModel, QuestionnaireAdmin)

