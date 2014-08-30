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

    def test_flatten_address_list(self):
        d = {'foo': [1, 2, 3], 'bar': [456]}
        result = util._flatten_address_list(d)
        expected = [1, 2, 3, 456]

        self.assertItemsEqual(expected, result)

    def test_hash_addresses(self):
        result = util.hash_addresses(self._servers, self._addresses)
        expected = {
            'mocked-3.example.com': ['2.2.2.2', '3.3.3.3'],
            'mocked-1.example.com': ['1.1.1.1']
        }

        self.assertEquals(expected, result)

    def test_all_addresses(self):
        result = util.all_addresses(self._servers, self._addresses)
        expected = ['1.1.1.1', '2.2.2.2', '3.3.3.3']

        self.assertItemsEqual(expected, result)

    def test_my_addresses(self):
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.my_addresses(self._servers, self._addresses)
            expected = ['2.2.2.2', '3.3.3.3']

            self.assertItemsEqual(expected, result)

    def test_my_addresses_returns_empty_list(self):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.my_addresses(servers, addresses)

        self.assertEquals([], result)

    def test_not_my_addresses(self):
        addresses = ['1.1.1.1', '2.1.1.1', '3.1.1.1', '4.1.1.1',
                     '5.1.1.1', '6.1.1.1', '7.1.1.1', '8.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-3.example.com'
            result = util.not_my_addresses(self._servers, addresses)
            expected = ['1.1.1.1', '3.1.1.1', '2.1.1.1',
                        '4.1.1.1', '5.1.1.1', '7.1.1.1']

            self.assertItemsEqual(expected, result)

    def test_not_my_addresses_returns_empty_list(self):
        servers = ['mocked-1.example.com']
        addresses = ['1.1.1.1']
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-1.example.com'
            result = util.not_my_addresses(servers, addresses)

            self.assertEquals([], result)
