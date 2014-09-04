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

    def test_get_hostname(self):
        with patch('socket.getfqdn') as mocked:
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

    def test_get_own_addresses(self):
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.get_own_addresses(self._servers, self._addresses)
            expected = ['2.2.2.2', '3.3.3.3']

            self.assertItemsEqual(expected, result)

    def test_get_own_addresses_returns_empty_list(self):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.get_own_addresses(servers, addresses)

        self.assertEquals([], result)

    def test_get_other_addresses(self):
        addresses = ['1.1.1.1', '2.1.1.1', '3.1.1.1', '4.1.1.1',
                     '5.1.1.1', '6.1.1.1', '7.1.1.1', '8.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.get_other_addresses(self._servers, addresses)
            expected = ['1.1.1.1', '3.1.1.1', '2.1.1.1',
                        '4.1.1.1', '5.1.1.1', '7.1.1.1']

            self.assertItemsEqual(expected, result)

    def test_get_other_addresses_returns_empty_list(self):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-1.example.com'
            result = util.get_other_addresses(servers, addresses)

            self.assertEquals([], result)

    def test_execute_returns_exitcode_tuple(self):
        cmd = 'test true'
        result, _, _ = util.execute(cmd)

        self.assertEquals(0, result)

    def test_execute_returns_stdout_tuple(self):
        cmd = 'echo stdout'
        _, out, _ = util.execute(cmd)

        self.assertEquals('stdout\n', out)

    def test_execute_returns_stderr_tuple(self):
        cmd = 'echo stderr >&2'
        _, _, err = util.execute(cmd)

        self.assertEquals('stderr\n', err)

    def test_add_alias_command_for_darwin(self):
        with patch('platform.system') as mocked:
            mocked.return_value = 'Darwin'
            result = util.add_alias_command('10.0.0.1/24', 'eth1', 'eth1:10')
            expected = 'ifconfig eth1 alias 10.0.0.1/24'

            self.assertEquals(expected, result)

    def test_add_alias_command_for_linux(self):
        with patch('platform.system') as mocked:
            mocked.return_value = 'Linux'
            result = util.add_alias_command('10.0.0.1/24', 'eth1', 'eth1:10')
            expected = 'ip addr add 10.0.0.1/24 dev eth1 label eth1:10'

            self.assertEquals(expected, result)

    def test_add_alias(self):
        with patch('tribe.util.get_alias') as mocked_get_alias:
            mocked_get_alias.return_value = False
            with patch('tribe.util.execute') as mocked:
                mocked.return_value = (0, Mock(), Mock())
                util.add_alias('10.0.0.1/24', 'eth1', 'eth1:10')

                mocked.assert_called_once

    def test_does_not_add_alias(self):
        with patch('tribe.util.get_alias') as mocked_get_alias:
            mocked_get_alias.return_value = True
            with patch('tribe.util.execute') as mocked:

                assert not mocked.called

    def test_delete_alias_command_for_darwin(self):
        with patch('platform.system') as mocked:
            mocked.return_value = 'Darwin'
            result = util.delete_alias_command('10.0.0.1/24',
                                               'eth1',
                                               'eth1:10')
            expected = 'ifconfig eth1 -alias 10.0.0.1'

            self.assertEquals(expected, result)

    def test_delete_alias_command_for_linux(self):
        with patch('platform.system') as mocked:
            mocked.return_value = 'Linux'
            result = util.delete_alias_command('10.0.0.1/24',
                                               'eth1',
                                               'eth1:10')
            expected = 'ip addr del 10.0.0.1/24 dev eth1 label eth1:10'

            self.assertEquals(expected, result)

    def test_delete_alias(self):
        with patch('tribe.util.get_alias') as mocked_get_alias:
            mocked_get_alias.return_value = False
            with patch('tribe.util.execute') as mocked:
                mocked.return_value = (0, Mock(), Mock())
                util.delete_alias('10.0.0.1/24', 'eth1', 'eth1:10')

                mocked.assert_called_once

    def test_does_not_delete_alias(self):
        with patch('tribe.util.get_alias') as mocked_get_alias:
            mocked_get_alias.return_value = True
            with patch('tribe.util.execute') as mocked:

                assert not mocked.called

    def test_get_alias(self):
        with patch('netifaces.ifaddresses') as mocked:
            mocked.return_value = True
            result = util.get_alias('valid')

            self.assertEquals(True, result)

    def test_get_alias_with_invalid_dev(self):
        result = util.get_alias('invalid')

        self.assertEquals(False, result)
