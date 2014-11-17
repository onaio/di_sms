#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from rapidsms.tests.harness import RapidTest


class TestSMSSyncBackendView(RapidTest):
    def setUp(self):
        self.valid_data = {
            'from': '12345',
            'message': 'help',
            'device_id': 'minidroid'
        }
        self.smssync_url = reverse('smssync-backend')

    def test_valid_post(self):
        response = self.client.post(self.smssync_url, self.valid_data)
        self.assertEqual(response.status_code, 200)

        data = {"payload": {"secret": "ona", "success": True, "error": None}}
        self.assertEqual(json.loads(response.content), data)
