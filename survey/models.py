from django.db import models
from profiles.models import Profile

opt_1 = "Very inaccurate"
opt_2 = "Moderately Inaccurate"
opt_3 = "Neither Accurate Nor Inaccurate"
opt_4 = "Moderately Accurate"
opt_5 = "Very Accurate"
answer_choices = ((1, opt_1), (2, opt_2), (3, opt_3), (4, opt_4), (5, opt_5))
type_of_question = (("Extraversion", "Extr."), ("Agreeableness", "Agree."),
                        ("Conscientiousness", "Consc."), ("Emotional Stability", "Emot."),
                        ("Intellect", "Intel"))


class Survey(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class QuestionIpip(models.Model):
    survey = models.ForeignKey(Survey)
    question_number = models.IntegerField()
    question = models.CharField(max_length=200)
    #Scoring use
        # Weight of the answer in the score
    question_weight = models.CharField(max_length=1, choices=(("+", "+"), ("-", "-")))
    type = models.CharField(max_length=20, choices=type_of_question)



    def __str__(self):
        return self.question

    class Meta:
        unique_together = ["survey", "question_number"]


class AnswersIpipCompleted(models.Model):
    profile = models.ForeignKey(Profile)
    survey = models.ForeignKey(Survey)

    def __str__(self):
        text = str(self.survey) + " " + str(self.profile)
        return text


class OneAnswerIpip(models.Model):
    question = models.ForeignKey(QuestionIpip)
    all_answers = models.ForeignKey(AnswersIpipCompleted)
    answer_value = models.IntegerField(choices=answer_choices, blank=True, null=True)

    @property
    def score(self):
        if self.question.question_weight == "-":
            if self.answer_value == 1:
                value = 5
            elif self.answer_value == 2:
                value = 4
            elif self.answer_value == 3:
                value = 3
            elif self.answer_value == 4:
                value = 2
            elif self.answer_value == 5:
                value = 1
        else:
            value = self.answer_value
        return value


