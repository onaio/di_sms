from django.contrib import admin

from .models import Section
from .models import Question
from .models import Answer

import reversion


class SectionAdmin(reversion.VersionAdmin):
    pass


class QuestionAdmin(reversion.VersionAdmin):
    pass


class AnswerAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
