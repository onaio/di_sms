from django import forms

from rapidsms.backends.http.forms import BaseHttpForm


class SmsSyncForm(BaseHttpForm):
    sent_to = forms.CharField()

    def __init__(self, *args, **kwargs):
        """
        Saves the identity (phone number) and text field names on self, calls
        super(), and then adds the required fields.
        """
        # defaults to "text" and "identity"
        self.text_name = kwargs.pop('text_name', 'text')
        self.identity_name = kwargs.pop('identity_name', 'identity')
        super(SmsSyncForm, self).__init__(*args, **kwargs)
        self.fields[self.text_name] = forms.CharField()
        self.fields[self.sent_to_name] = forms.CharField()

    def get_incoming_data(self):
        """
        Returns the connection and text for this message, based on the field
        names passed to __init__().
        """
        fields = self.cleaned_data.copy()
        identity = self.cleaned_data[self.identity_name]
        connections = self.lookup_connections([identity])
        return {'connection': connections[0],
                'text': self.cleaned_data[self.text_name],
                'fields': fields}
