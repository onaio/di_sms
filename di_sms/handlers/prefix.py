#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django.utils.translation import ugettext as _
from rapidsms.contrib.handlers import BaseHandler
from rapidsms.contrib.handlers.exceptions import HandlerError


class PrefixHandler(BaseHandler):
    prefix = None
    pattern = r'%(prefix)s\s?(\w+.*?)(?=\s*%(prefix)s|$)'

    def handle(self, question, answer):
        self.respond(
            _(u"Vous avez répondu à la question numéro {}, votre réponse "
              u"était \"{}\".")
            .format(question, answer)
        )

    @classmethod
    def _pattern(cls):
        if not hasattr(cls, "prefix"):
            raise HandlerError('PrefixHandler must define a prefix')

        if hasattr(cls, "pattern") and cls.pattern and cls.prefix:
            return re.compile(cls.pattern % {'prefix': cls.prefix},
                              re.IGNORECASE)

        raise HandlerError('PrefixHandler must define a pattern.')

    @classmethod
    def dispatch(cls, router, msg):
        pattern = cls._pattern()

        match = pattern.match(msg.text)
        if match is None:
            return False

        cls(router, msg).handle(pattern.findall(msg.text))

        return True
