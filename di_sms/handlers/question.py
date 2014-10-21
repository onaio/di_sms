from django.utils.translation import ugettext as _
from rapidsms.contrib.handlers import PatternHandler


class QuestionHandler(PatternHandler):
    pattern = r'^#(\d+) (.*)$'

    def handle(self, question, answer):
        self.respond(
            _(u"You responded to question number {}, your answer was \"{}\".")
            .format(question, answer)
        )
