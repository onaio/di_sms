from django.utils.translation import ugettext as _
from rapidsms.contrib.handlers import KeywordHandler


class HelpHandler(KeywordHandler):
    keyword = "help"

    def help(self):
        msg = _(u"Help! Expected commands are #1 answer1 #2 answer2 ...")
        self.respond(msg)

    def handle(self, text):
        self.help()
