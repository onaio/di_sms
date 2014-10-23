from rapidsms.messages import IncomingMessage
from rapidsms.tests.harness import RapidTest

from di_sms.handlers.help import HelpHandler


class TestHelpHandler(RapidTest):
    def setUp(self):
        self.connection = self.create_connection()

    def test_dispatch(self):
        response = "Help! Expected commands are ... "
        msg = IncomingMessage([self.connection], "help")
        retVal = HelpHandler.dispatch(self.router, msg)
        self.assertTrue(retVal)
        self.assertEqual(len(msg.responses), 1)
        self.assertEqual(msg.responses[0]['text'], response)
