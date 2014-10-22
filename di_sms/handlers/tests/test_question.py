from rapidsms.messages import IncomingMessage
from rapidsms.tests.harness import RapidTest

from di_sms.handlers.question import QuestionHandler


class TestHelpHandler(RapidTest):
    def setUp(self):
        self.connection = self.create_connection()

    def test_dispatch(self):
        response = 'You responded to 1 question(s).'
        msg = IncomingMessage(self.connection, "#1 y")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)

        response = 'You responded to 2 question(s).'
        msg = IncomingMessage(self.connection, "#1 y #34 n")
        retVal = QuestionHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
