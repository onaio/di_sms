from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Question(models.Model):
    YES_NO = "YN"
    TEXT = "TXT"
    NUMBER = "N"

    QUESTION_TYPE_CHOICES = (
        (YES_NO, "Yes or No"),
        (TEXT, "Free form text"),
        (NUMBER, "Number")
    )

    question = models.TextField()
    number = models.IntegerField()
    question_type = models.CharField(max_length=3,
                                     choices=QUESTION_TYPE_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    section = models.ForeignKey('Section')
    question = models.ForeignKey('Question')
    answer = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
