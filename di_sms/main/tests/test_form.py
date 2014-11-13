#!/usr/bin/python
# -*- coding: utf-8 -*-

from rapidsms.tests.harness import RapidTest

from di_sms.main.forms import SmsSyncForm


class TestSMSSyncForm(RapidTest):
    def setUp(self):
        self.valid_data = {
            'text': '12345',
            'identity': 'help',
            'device_id': 'minidroid'
        }

    def test_valid_form(self):
        form = SmsSyncForm(self.valid_data, backend_name='smssync')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = SmsSyncForm({'invalid-text': 'hello'}, backend_name='smssync')
        self.assertFalse(form.is_valid())

    def test_get_incoming_data(self):
        form = SmsSyncForm(self.valid_data, backend_name='smssync')
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(self.valid_data['identity'],
                         incoming_data['fields']['identity'])
        self.assertEqual(self.valid_data['text'], incoming_data['text'])
        self.assertEqual(self.valid_data['device_id'],
                         incoming_data['fields']['device_id'])
