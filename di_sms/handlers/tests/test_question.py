#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.core.management import call_command

from rapidsms.messages import IncomingMessage
from rapidsms.tests.harness import RapidTest

from di_sms.handlers.question import QuestionHandler
from di_sms.main import tests as main_tests
from di_sms.main.models import Answer
from di_sms.main.models import Question


class TestQuestionHandler(RapidTest):
    def setUp(self):
        self.contact = self.create_contact()
        self.connections = self.lookup_connections(['+12344243'])
        self.connections[0].contact = self.contact

    def _load_questions_fixture(self):
        fixture_path = os.path.join(
            os.path.dirname(main_tests.__file__), 'fixtures', 'questions.json')

        if not os.path.exists(fixture_path):
            raise Exception('{} does not exist.'.format(fixture_path))

        call_command('loaddata', fixture_path)

    def test_dispatch_question(self):
        count = Answer.objects.count()
        self._load_questions_fixture()
        response0 = u'opening1 is missing question(s): 2,3.'
        response1 = u'You responded to question(s): 1.'
        msg = IncomingMessage(self.connections, "#1 y")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 2)
        self.assertEqual(msg.responses[0]['text'], response0)
        self.assertEqual(msg.responses[1]['text'], response1)
        self.assertEqual(count + 1, Answer.objects.count())
        self.assertEqual(Answer.objects.all()[0].answer, Question.YES)

        response0 = u'opening1 is missing question(s): 2.'
        response1 = u'You responded to question(s): 1,3.'
        msg = IncomingMessage(self.connections, "#1 y #3 1")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 2)
        self.assertEqual(msg.responses[0]['text'], response0)
        self.assertEqual(msg.responses[1]['text'], response1)
        self.assertEqual(count + 2, Answer.objects.count())
        self.assertEqual(Answer.objects.all()[1].answer, u'1')

        response = u'You responded to question(s): 1,2,3.'
        msg = IncomingMessage(self.connections, "#1 y #2 n #3 1")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count + 3, Answer.objects.count())
        self.assertEqual(Answer.objects.all()[2].answer, Question.NO)

        response = u'Unknown question number 34.'
        msg = IncomingMessage(self.connections, "#1 y #34 n")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count + 3, Answer.objects.count())

    def test_dispatch_unknown_question(self):
        response = u'Unknown question number 1.'
        msg = IncomingMessage(self.connections, "#1 y")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)

        response = u'Unknown question number 1.'
        response += u' Unknown question number 34.'
        msg = IncomingMessage(self.connections, "#1 y #34 n")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)

    def test_dispatch_question_invalid_yes_no_answer(self):
        count = Answer.objects.count()
        self._load_questions_fixture()
        response = u'Invalid answer k, expecting Y or N.'
        msg = IncomingMessage(self.connections, u"#1 k")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count, Answer.objects.count())

    def test_dispatch_question_not_a_number(self):
        count = Answer.objects.count()
        self._load_questions_fixture()
        response = u'k is not a number.'
        msg = IncomingMessage(self.connections, u"#3 k")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count, Answer.objects.count())
