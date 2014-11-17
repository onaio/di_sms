#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import uuid

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from rapidsms.contrib.handlers.exceptions import HandlerError

from di_sms.handlers.prefix import PrefixHandler
from di_sms.main.models import Answer
from di_sms.main.models import Question
from di_sms.main.utils import make_ona_submission

YES_NO_REGEX = re.compile('([ynYN])', re.IGNORECASE)
YES_REGEX = re.compile('([yY])', re.IGNORECASE)
NUMBER_REGEX = re.compile('(^[0-9]+(\.[0-9]+)*)')


class QuestionHandler(PrefixHandler):
    prefix = '#'

    def handle(self, answers):
        self.phone_number = self.msg.connections[0].identity
        self.device_id = self.msg.fields.get('device_id')

        if self._valid_questions(answers):
            responses = []
            qa = []
            for question, answer in self.question_answers:
                qa.append(self._save_answer(question, answer).pk)
                responses.append(str(question.number))

            self._make_ona_submission(qa)

            self.respond(
                _(u"You responded to question(s): {}.").format(
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
        pattern = r'(?P<number>\d+)\s*(?P<answer>\w+)'
        qa_regex = re.compile(pattern, re.IGNORECASE)
        match = re.match(qa_regex, text)

        if match:
            answer = match.groupdict()['answer'].strip()
            question = match.groupdict()['number']

            try:
                question = Question.objects.get(number=question)
            except Question.DoesNotExist:
                raise ValueError(
                    _(u"Unknown question number {}.").format(question))
            else:
                if question.question_type == Question.YES_NO:
                    if not YES_NO_REGEX.match(answer):
                        raise ValueError(
                            _(u"Invalid answer {}, expecting Y or N.")
                            .format(answer))

                    if YES_REGEX.match(answer):
                        answer = Question.YES
                    else:
                        answer = Question.NO

                if question.question_type == Question.NUMBER:
                    if not NUMBER_REGEX.match(answer):
                        raise ValueError(_(u"{} is not a number.")
                                         .format(answer))

                return question, answer

        raise HandlerError(
            _(u"Unknown question {}.").format(text))

    def _save_answer(self, question, answer):
        if not self.msg.connections:
            raise ValueError

        answer, created = Answer.objects.get_or_create(
            phone_number=self.phone_number, question=question, answer=answer)

        return answer

    @classmethod
    def _submission_xml(cls, answers_qs, section_name, context={}):
        if not answers_qs.count():
            return u''

        qa = answers_qs.values_list('question__number', 'answer')
        context['section'] = section_name
        context['today'] = unicode(answers_qs[0].date_created.date())
        context['instanceID'] = u"uuid:{}".format(uuid.uuid4())
        context['question_answer'] = qa
        xml = render_to_string('section.xml', context).strip()
        xml = re.sub(ur">\s+<", u"><", smart_unicode(xml))

        return xml

    def _valid_section(self, answers):
        count = answers.count()

        if count:
            answered = answers.values_list('question', flat=True)
            section = answers[0].question.section

            section_qs = Question.objects.filter(section=section)

            self.missing = [
                unicode(q) for q in section_qs.exclude(pk__in=answered)
                .values_list('number', flat=True)]

            return count == section_qs.count()

        return True

    def _make_ona_submission(self, answers):
        answer_qs = Answer.objects.filter(
            pk__in=answers, phone_number=self.phone_number).select_related()
        sections = answer_qs.values_list('question__section',
                                         'question__section__name').distinct()
        context = {
            "phone_number": self.phone_number,
            "device_id": self.device_id
        }
        url = settings.ONA_SUBMISSION_URL

        for section_id, section_name in sections:
            qa = answer_qs.filter(question__section=section_id)
            if self._valid_section(qa):
                xml_str = self._submission_xml(qa, section_name, context)
                make_ona_submission(url, xml_str)
            else:
                self.respond(_(u"{} is missing question(s): {}.")
                             .format(section_name, u','.join(self.missing)))
