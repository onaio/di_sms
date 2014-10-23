#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import uuid

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from rapidsms.contrib.handlers.exceptions import HandlerError

from di_sms.handlers.prefix import PrefixHandler
from di_sms.main.models import Answer
from di_sms.main.models import Question
from di_sms.main.utils import make_ona_submission

YES_NO_REGEX = re.compile('([ynmYNoO0])', re.IGNORECASE)


class QuestionHandler(PrefixHandler):
    prefix = '#'

    def handle(self, answers):
        self.phone_number = self.msg.connections.identity

        if self._valid_questions(answers):
            responses = []
            qa = []
            for question, answer in self.question_answers:
                qa.append(self._save_answer(question, answer).pk)
                responses.append(str(question.number))

            self._make_ona_submission(qa)

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

        answer, created = Answer.objects.get_or_create(
            phone_number=self.phone_number, question=question, answer=answer)

        return answer

    @classmethod
    def _submission_xml(cls, answers, section_id, section_name, context={}):
        qa = answers.filter(question__section=section_id)\
            .values_list('question__number', 'answer')
        context['section'] = section_name
        context['today'] = unicode(timezone.now().date())
        context['instanceID'] = uuid.uuid4()
        context['question_answer'] = qa
        xml = render_to_string('section.xml', context).strip()
        xml = re.sub(ur">\s+<", u"><", smart_unicode(xml))

        return xml

    def _make_ona_submission(self, answers):
        # get answers per section
        # generate xml submission
        # make submission to ona.io
        answer_qs = Answer.objects.filter(pk__in=answers)
        sections = answer_qs.values_list('question__section',
                                         'question__section__name')
        context = {
            "phone_number": self.phone_number
        }
        url = settings.ONA_SUBMISSION_URL

        for section_id, section_name in sections:
            xml_str = self._submission_xml(
                answer_qs, section_id, section_name, context)
            make_ona_submission(url, xml_str)
