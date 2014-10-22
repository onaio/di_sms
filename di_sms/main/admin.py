from django.contrib import admin

from .models import Section
from .models import Question
from .models import Answer

admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Answer)
