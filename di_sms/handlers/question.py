from rapidsms.contrib.handlers import PatternHandler


class QuestionHandler(PatternHandler):
    pattern = r'^q(\d+) (.*)$'

    def handle(self, question, answer):
        self.respond(
            u"You responded to question number {}, your answer was \"{}\"."
            .format(question, answer)
        )
