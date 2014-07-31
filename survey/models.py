from django.db import models

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
    question_weight = models.IntegerField()  # Weight of the answer in the score
    type = models.CharField(max_length=20, choices=type_of_question)
    answer_value = models.IntegerField(choices=answer_choices, blank=True, null=True)  # The user answer

    def __str__(self):
        return self.question

    class Meta:
        unique_together = ["survey", "question_number"]
