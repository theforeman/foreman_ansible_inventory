# vim: set fileencoding=utf-8 :

import responses
import unittest
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from foreman_ansible_inventory import ForemanInventory


class TestGetJson(unittest.TestCase):
    def setUp(self):
        self.inv = ForemanInventory()
        self.inv.foreman_url = 'http://localhost:3000'
        self.inv.foreman_user = 'doesnot'
        self.inv.foreman_pw = 'mastter'
        self.inv.foreman_ssl_verify = True

    def assertEqualUrl(self, url1, url2):
        p1 = urlparse.urlparse(url1)
        p2 = urlparse.urlparse(url2)
        q1 = urlparse.parse_qs(p1.query)
        q2 = urlparse.parse_qs(p2.query)
        self.assertEqual(p1.scheme, p2.scheme)
        self.assertEqual(p1.netloc, p2.netloc)
        self.assertEqual(p1.path, p2.path)
        self.assertEqual(p1.params, p2.params)
        self.assertEqual(p1.fragment, p2.fragment)
        self.assertEqual(q1, q2)

    @responses.activate
    def test_get_hosts(self):
        url = 'http://localhost:3000/api/v2/hosts'
        responses.add(responses.GET,
                      url,
                      json={'results': [{'name': 'foo'},
                                        {'name': 'bar'}],
                            'total': 4},
                      status=200)

        ret = self.inv._get_hosts()
        self.assertEqual(ret,
                         [{u'name': u'foo'},
                          {u'name': u'bar'},
                          {u'name': u'foo'},
                          {u'name': u'bar'}])
        self.assertEqual(len(responses.calls), 2)
        self.assertEqualUrl(responses.calls[0].request.url,
                            '%s?per_page=250&page=1' % url)
        self.assertEqualUrl(responses.calls[1].request.url,
                            '%s?per_page=250&page=2' % url)

    @responses.activate
    def test_get_facts(self):
        self.inv.want_facts = True
        url = 'http://localhost:3000/api/v2/hosts/10/facts'
        responses.add(responses.GET,
                      url,
                      json={'results': {'facts': {'fact1': 'val1',
                                                  'fact2': 'val2',
                                                  }
                                        },
                            },
                      status=200)

        ret = self.inv._get_facts({'id': 10})
        self.assertEqual(ret, {u'fact2': u'val2', u'fact1': u'val1'})
        self.assertEqual(len(responses.calls), 1)
        self.assertEqualUrl(responses.calls[0].request.url,
                            '%s?per_page=250&page=1' % url)

    @responses.activate
    def test_resolve_params(self):
        url = 'http://localhost:3000/api/v2/hosts/10'
        responses.add(responses.GET,
                      url,
                      json={'all_parameters':
                            [{'name': 'param1',
                              'value': 'value1'},
                             {'name': 'param2',
                              'value': 'value2'}]},
                      status=200)

        ret = self.inv._resolve_params({'id': 10})
        self.assertEqual(sorted(ret.items()),
                         sorted({'param1': 'value1',
                                 'param2': 'value2'}.items()))
        self.assertEqual(len(responses.calls), 1)

        self.assertEqualUrl(responses.calls[0].request.url,
                            '%s?per_page=250&page=1' % url)
