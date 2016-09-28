# vim: set fileencoding=utf-8 :

from __future__ import print_function


import os
import unittest
import tempfile

from foreman_ansible_inventory import ForemanInventory


class TestReadSettings(unittest.TestCase):
    def setUp(self):
        self.inv = ForemanInventory()

    def test_parse_nonexistent(self):
        os.environ['FOREMAN_INI_PATH'] = '/doesnot/exist'
        self.inv.config_paths = []
        self.assertFalse(self.inv.read_settings())

    def test_parse_params(self):
        with tempfile.NamedTemporaryFile() as t:
            print("""
[foreman]
url=http://127.0.0.1
user=admin
password=secret
ssl_verify=True
            """, file=t)
            t.flush()
            os.environ['FOREMAN_INI_PATH'] = t.name
            self.inv.config_paths = []
            self.assertTrue(self.inv.read_settings())
        self.assertEqual(self.inv.foreman_url, 'http://127.0.0.1')
        self.assertEqual(self.inv.foreman_user, 'admin')
        self.assertEqual(self.inv.foreman_pw, 'secret')
        self.assertTrue(self.inv.foreman_ssl_verify)
