import re

from django.utils.translation import ugettext as _
from rapidsms.contrib.handlers.exceptions import HandlerError

from di_sms.handlers.prefix import PrefixHandler
from di_sms.main.models import Answer
from di_sms.main.models import Question


class QuestionHandler(PrefixHandler):
    prefix = '#'

    def handle(self, answers):
        if self._valid_questions(answers):
            for answer in self.question_answers:
                self._save_answer(*answer)

            self.respond(
                _(u"You responded to {} question(s).").format(len(answers))
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
                    _("Unknown question number {}.").format(question))
            else:
                return question, answer

        raise HandlerError(_("Unknown question answer {}.").format(text))

    def _save_answer(self, question, answer):
        if not self.msg.connections:
            raise ValueError

        contact = self.msg.connections[0].contact

        Answer.objects.get_or_create(
            contact=contact, question=question, answer=answer)
