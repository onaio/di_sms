#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.core.management import call_command

from rapidsms.messages import IncomingMessage
from rapidsms.tests.harness import RapidTest

from di_sms.handlers.question import QuestionHandler
from di_sms.main import tests as main_tests
from di_sms.main.models import Answer


class TestHelpHandler(RapidTest):
    def setUp(self):
        self.contact = self.create_contact()
        self.connection = self.lookup_connections(['+12344243'])[0]
        self.connection.contact = self.contact

    def _load_questions_fixture(self):
        fixture_path = os.path.join(
            os.path.dirname(main_tests.__file__), 'fixtures', 'questions.json')

        if not os.path.exists(fixture_path):
            raise Exception('{} does not exist.'.format(fixture_path))

        call_command('loaddata', fixture_path)

    def test_dispatch_question(self):
        count = Answer.objects.count()
        self._load_questions_fixture()
        response = 'Vous avez répondu à la/les question(s): 1.'
        msg = IncomingMessage(self.connection, "#1 y")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count + 1, Answer.objects.count())

        response = 'Vous avez répondu à la/les question(s): 1,3.'
        msg = IncomingMessage(self.connection, "#1 y #3 N")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count + 2, Answer.objects.count())

        response = 'Inconnu numéro de la question 34.'
        msg = IncomingMessage(self.connection, "#1 y #34 n")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
        self.assertEqual(count + 2, Answer.objects.count())

    def test_dispatch_unknown_question(self):
        response = 'Inconnu numéro de la question 1.'
        msg = IncomingMessage(self.connection, "#1 y")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)

        response = 'Inconnu numéro de la question 1.'
        response += ' Inconnu numéro de la question 34.'
        msg = IncomingMessage(self.connection, "#1 y #34 n")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
