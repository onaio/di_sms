from rapidsms.contrib.handlers import KeywordHandler


class HelpHandler(KeywordHandler):
    keyword = "help"

    def help(self):
        self.respond(u"Help! Expected commands are ... ")

    def handle(self, text):
        # text = text.strip.lower()

        self.help()
