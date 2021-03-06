# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2014 John Dewey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import unittest2 as unittest
from mock import Mock
from mock import patch

from tribe import util


class TestUtil(unittest.TestCase):
    def setUp(self):
        self._servers = ['mocked-1.example.com',
                         'mocked-2.example.com',
                         'mocked-3.example.com']
        self._addresses = ['1.1.1.1',
                           '2.2.2.2',
                           '3.3.3.3']

    @patch('socket.getfqdn')
    def test_get_hostname(self, mocked):
        mocked.return_value = 'mocked-fqdn'
        result = util.get_hostname()

        self.assertEquals('mocked-fqdn', result)

    def test_hash_addresses(self):
        result = util.hash_addresses(self._servers, self._addresses)
        expected = {
            'mocked-3.example.com': ['2.2.2.2', '3.3.3.3'],
            'mocked-1.example.com': ['1.1.1.1']
        }

        self.assertEquals(expected, result)

    @patch('socket.getfqdn')
    def test_get_own_addresses(self, mocked):
        mocked.return_value = 'mocked-3.example.com'
        result = util.get_own_addresses(self._servers, self._addresses)
        expected = ['2.2.2.2', '3.3.3.3']

        self.assertItemsEqual(expected, result)

    @patch('socket.getfqdn')
    def test_get_own_addresses_returns_empty_list(self, mocked):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        mocked.return_value = 'mocked-3.example.com'
        result = util.get_own_addresses(servers, addresses)

        self.assertEquals([], result)

    @patch('socket.getfqdn')
    def test_get_other_addresses(self, mocked):
        addresses = ['1.1.1.1', '2.1.1.1', '3.1.1.1', '4.1.1.1',
                     '5.1.1.1', '6.1.1.1', '7.1.1.1', '8.1.1.1']
        mocked.return_value = 'mocked-3.example.com'
        result = util.get_other_addresses(self._servers, addresses)
        expected = ['1.1.1.1', '3.1.1.1', '2.1.1.1',
                    '4.1.1.1', '5.1.1.1', '7.1.1.1']

        self.assertItemsEqual(expected, result)

    @patch('socket.getfqdn')
    def test_get_other_addresses_returns_empty_list(self, mocked):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        mocked.return_value = 'mocked-1.example.com'
        result = util.get_other_addresses(servers, addresses)

        self.assertEquals([], result)

    def test_execute(self):
        cmd = ['test', 'true']
        result = util.execute(cmd)

        self.assertEquals(True, result)

    def test_execute_raises(self):
        cmd = ['ls', '/invalid']
        with self.assertRaises(Exception) as context:
            util.execute(cmd)

        # OSX:
        # ls: /invalid: No such file or directory\n
        # Travis:
        # ls: cannot access /invalid: No such file or directory\n
        self.assertRegexpMatches(context.exception.message,
                                 r'.* No such file or directory\n')

    def test_get_alias_label(self):
        result = util._get_alias_label('eth1', '192.168.20.203/32')

        self.assertEquals('eth1:203', result)

    @patch('tribe.util.get_alias')
    @patch('tribe.util.execute')
    def test_add_alias(self, mocked_execute, mocked_get_alias):
        mocked_get_alias.return_value = False
        mocked_execute.return_value = (0, Mock(), Mock())
        util.add_alias('10.0.0.1/32', 'eth1')
        cmd = ['/bin/ip', 'addr', 'add', '10.0.0.1/32',
               'dev', 'eth1',
               'label', 'eth1:1']

        mocked_execute.assert_called_once_with(cmd)

    @patch('tribe.util.get_alias')
    @patch('tribe.util.execute')
    def test_does_not_add_alias(self, mocked_execute, mocked_get_alias):
        mocked_get_alias.return_value = True

        assert not mocked_execute.called

    @patch('tribe.util.get_alias')
    @patch('tribe.util.execute')
    def test_delete_alias(self, mocked_execute, mocked_get_alias):
        mocked_get_alias.return_value = True
        mocked_execute.return_value = (0, Mock(), Mock())
        util.delete_alias('10.0.0.1/32', 'eth1')
        cmd = ['/bin/ip', 'addr', 'del', '10.0.0.1/32',
               'dev', 'eth1']

        mocked_execute.assert_called_once_with(cmd)

    @patch('tribe.util.get_alias')
    @patch('tribe.util.execute')
    def test_does_not_delete_alias(self, mocked_execute, mocked_get_alias):
        mocked_get_alias.return_value = False

        assert not mocked_execute.called

    @patch('netifaces.ifaddresses')
    def test_get_alias(self, mocked):
        mocked.return_value = {}
        result = util.get_alias('eth1:valid')

        self.assertEquals(True, result)

    @patch('netifaces.ifaddresses')
    def test_get_alias_with_invalid_dev(self, mocked):
        mocked.side_effect = ValueError
        result = util.get_alias('eth1:invalid')

        self.assertEquals(False, result)
