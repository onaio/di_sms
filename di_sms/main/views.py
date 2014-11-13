import json
import uuid

from django.http.response import HttpResponse
from django.http.response import HttpResponseBadRequest
from rapidsms.backends.database.models import BackendMessage
from rapidsms.backends.database.models import OUTGOING
from rapidsms.backends.http.views import GenericHttpBackendView

from di_sms.main.forms import SmsSyncForm


class SmsSyncBackendView(GenericHttpBackendView):
    params = {
        'identity_name': 'from',
        'device_identity': 'device_id',
        'text_name': 'message'
    }

    # Form to validate that received parameters match defined ``params``.
    form_class = SmsSyncForm

    def form_valid(self, form):
        super(SmsSyncBackendView, self).form_valid(form)
        data = {
            "payload": {
                "secret": "ona",
                "success": True,
                "error": None
            }
        }

        return HttpResponse(json.dumps(data), content_type='application/json')

    def form_invalid(self, form):
        super(SmsSyncBackendView, self).form_invalid(form)
        data = {
            "payload": {
                "secret": "ona",
                "success": False,
                "error": 'Form failed to validate'
            }
        }

        return HttpResponseBadRequest(json.dumps(data),
                                      content_type='application/json')

    def get(self, request, *args, **kwargs):
        task = request.GET.get('task')

        if task and task.lower() == 'send':
            data = {
                "payload": {
                    "task": "send",
                    "secret": "ona",
                    "messages": self.get_outgoing_messages()
                }
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json')

        return HttpResponse()

    def get_outgoing_messages(self):
        data = []
        messages = BackendMessage.objects.filter(
            external_id='', direction=OUTGOING)

        for msg in messages:
            msg.external_id = uuid.uuid1().hex
            msg.save()
            data.append({"to": msg.identity, "message": msg.text})

        return data
