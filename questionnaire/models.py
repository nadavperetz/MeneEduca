# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

indicator_choices = (('Extroversion ', _('Extroversion (1)')),
                     ('Agreeableness', _('Agreeableness (2)')),
                     ('Conscientiousness', _('Conscientiousness (3)')),
                     ('Emotional Stability', _('Emotional Stability (4)')),
                     ('Intellect/Imagination', _('Intellect/Imagination (5)')))

answers = ((1, _('Very Inaccurate')),
           (2, _('Moderately Inaccurate')),
           (3, _('Neither Accurate Nor Inaccurate')),
           (4, _('Moderately Accurate')),
           (5, _('Very Accurate')))


indicator_weight = (('+', '+'),
                    ('-', '-'))


@python_2_unicode_compatible
class QuestionnaireModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class QuestionModel(models.Model):
    question = models.CharField(max_length=50, verbose_name=_("Question"))
    type_of_answer = models.CharField(max_length=30, verbose_name=_("Type of Factor"),
                                      choices=indicator_choices)
    weight = models.CharField(max_length=1, verbose_name=_("Weight"), choices=indicator_weight)
    questionnaire = models.ForeignKey(QuestionnaireModel)

    def __str__(self):
        return self.question


class QuestionnaireAnswered(models.Model):
    questionnaire = models.ForeignKey(QuestionnaireModel)
    student = models.ForeignKey('profiles.Student')
    finish = models.BooleanField(default=False)

    def values(self):
        dicionario = {}
        for choice in indicator_choices:
            dicionario[str(choice[0])] = 0
        print dicionario
        for question in self.questionanswered_set.all():
            print "Answer"
            print question.question.type_of_answer
            if question.question.weight == "-":
                if question.answer == '1':
                    dicionario[question.question.type_of_answer] += 5
                elif question.answer == '2':
                    dicionario[question.question.type_of_answer] += 4
                elif question.answer == '4':
                    dicionario[question.question.type_of_answer] += 2
                elif question.answer == '5':
                    dicionario[question.question.type_of_answer] += 1
                else:
                    dicionario[question.question.type_of_answer] += question.answer
            else:
                dicionario[question.question.type_of_answer] += question.answer
        print dicionario
        return dicionario

    def __str__(self):
        text = str(self.questionnaire) + " "
        text += str(self.student)
        return text


class QuestionAnswered(models.Model):
    question = models.ForeignKey(QuestionModel)
    answer = models.IntegerField(choices=answers, blank=True, null=True)
    questionnaire = models.ForeignKey(QuestionnaireAnswered)
    answered = models.BooleanField(default=False)





