from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    YES_NO = "YN"
    YES = 'yes'
    NO = 'no'
    TEXT = "TXT"
    NUMBER = "N"

    QUESTION_TYPE_CHOICES = (
        (YES_NO, "Yes or No"),
        (TEXT, "Free form text"),
        (NUMBER, "Number")
    )

    number = models.IntegerField(unique=True)
    section = models.ForeignKey('Section')
    question = models.TextField()
    question_type = models.CharField(max_length=3,
                                     choices=QUESTION_TYPE_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey('Question')
    answer = models.CharField(max_length=255, db_index=True)
    phone_number = models.CharField(max_length=100, db_index=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
