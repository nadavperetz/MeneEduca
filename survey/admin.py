from django.contrib import admin
from survey.models import Survey, QuestionIpip


class QuestionInline(admin.StackedInline):
    model = QuestionIpip
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)

# Register your models here.
