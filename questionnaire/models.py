from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

indicator_choices = (('1', _('Extroversion (1)')),
                     ('2', _('Agreeableness (2)')),
                     ('3', _('Conscientiousness (3)')),
                     ('4', _('Emotional Stability (4)')),
                     ('5', _('Intellect/Imagination (5)')))

answers = ((1, _('Very Inaccurate')),
           (2, _('Moderately Inaccurate')),
           (3, _('Neither Accurate Nor Inaccurate')),
           (4, _('Moderately Accurate')),
           (5, _('Very Accurate')))


indicator_weight = (('+', '+'),
                    ('-', '-'))


class QuestionnaireModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class QuestionModel(models.Model):
    question = models.CharField(max_length=50, verbose_name=_("Question"))
    type_of_answer = models.CharField(max_length=30, verbose_name=_("Type of Factor"),
                                      choices=indicator_choices)
    weight = models.CharField(max_length=1, verbose_name=_("Weight"), choices=indicator_weight)
    questionnaire = models.ForeignKey(QuestionnaireModel)

    def __str__(self):
        return self.question


class QuestionAnswered(models.Model):
    question = models.ForeignKey(QuestionModel)
    answer = models.IntegerField(choices=answers)


class QuestionnaireAnswered(models.Model):
    questionnaire = models.ForeignKey(QuestionnaireModel)
    student = models.ForeignKey('profiles.Student')
    answers = models.ManyToManyField(QuestionAnswered)

    def __str__(self):
        text = str(self.questionnaire) + " "
        text += str(self.student)
        return text



