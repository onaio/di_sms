from django.utils.translation import ugettext as _

from di_sms.handlers.prefix import PrefixHandler


class QuestionHandler(PrefixHandler):
    prefix = '#'

    def handle(self, answers):
        self.respond(
            _(u"You responded to {} question(s).").format(len(answers))
        )
