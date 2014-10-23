#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django.utils.translation import ugettext as _
from rapidsms.contrib.handlers.exceptions import HandlerError

from di_sms.handlers.prefix import PrefixHandler
from di_sms.main.models import Answer
from di_sms.main.models import Question

YES_NO_REGEX = re.compile('([ynmYNoO0])', re.IGNORECASE)


class QuestionHandler(PrefixHandler):
    prefix = '#'

    def handle(self, answers):
        if self._valid_questions(answers):
            responses = []
            for question, answer in self.question_answers:
                self._save_answer(question, answer)
                responses.append(str(question.pk))

            self.respond(
                _(u"Vous avez répondu à la/les question(s): {}.").format(
                    u','.join(responses))
            )
        else:
            self.respond(u' '.join(self._errors))

    def _valid_questions(self, answers):
        self._errors = []
        self.question_answers = []

        for answer in answers:
            try:
                self.question_answers.append(self._question_answer(answer))
            except ValueError as e:
                self._errors.append(unicode(e))

        return len(self._errors) == 0

    @classmethod
    def _question_answer(cls, text):
        pattern = r'(?P<number>\d+)\s(?P<answer>\w+)'
        qa_regex = re.compile(pattern, re.IGNORECASE)
        match = re.match(qa_regex, text)

        if match:
            answer = match.groupdict()['answer']
            question = match.groupdict()['number']

            try:
                question = Question.objects.get(number=question)
            except Question.DoesNotExist:
                raise ValueError(
                    _(u"Inconnu numéro de la question {}.").format(question))
            else:
                if question.question_type == Question.YES_NO:
                    if not YES_NO_REGEX.match(answer):
                        raise ValueError(
                            _(u"Inconnu numéro de la answer {}.")
                            .format(answer))
                return question, answer

        raise HandlerError(
            _(u"Inconnu numéro de la question {}.").format(text))

    def _save_answer(self, question, answer):
        if not self.msg.connections:
            raise ValueError

        phone_number = self.msg.connections.identity

        Answer.objects.get_or_create(
            phone_number=phone_number, question=question, answer=answer)
