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

import datetime
import multiprocessing
import os
import random
import string
import time

import unittest2 as unittest
from mock import patch
from nose.plugins.attrib import attr

from tribe import client
from tribe import config


class TestClient(unittest.TestCase):
    def _random_key(self, size=6, chars=string.ascii_letters):
        return ''.join(random.choice(chars) for x in range(size))

    def setUp(self):
        basedir = os.path.dirname(__file__)
        f = os.path.join(basedir, 'test.json')
        self._config = config.Config(config_file=f)
        self._client = client.Client(self._config)
        self._key = '/{0}'.format(self._random_key())
        self._sleep_time = 0.1

    def test_get_key(self):
        with patch('etcd.client.Client.read') as mocked:
            self._client.get_key('mocked-key')

            mocked.assert_called_once_with('mocked-key',
                                           recursive=False,
                                           wait=False)

    @attr('integration')
    def test_get_key_returns(self):
        self._client.add_key(self._key, 'value')
        time.sleep(self._sleep_time)

        result = self._client.get_key(self._key)
        self.assertEquals('value', result.value)

        self._client.delete_key(self._key)

    @attr('integration')
    def test_get_key_returns_list(self):
        keys = ['/{0}/bar'.format(self._key),
                '/{0}/baz'.format(self._key)]
        for key in keys:
            self._client.add_key(key, 'value')
        time.sleep(self._sleep_time)

        result = self._client.get_key(self._key, recursive=True)
        self.assertEquals(2, len(result))
        for index, key in enumerate(keys):
            self.assertEquals('value', result[index].value)

        for key in keys:
            self._client.delete_key(key)

    @attr('integration')
    def test_get_key_returns_empty_list(self):
        keys = ['/{0}/bar'.format(self._key),
                '/{0}/baz'.format(self._key)]
        for key in keys:
            self._client.add_key(key, 'value', ttl=1)
        time.sleep(2)  # keys should now be expired by the ttl

        result = self._client.get_key(self._key, recursive=True)
        self.assertEquals(0, len(result))

    def test_add_key(self):
        with patch('etcd.client.Client.set') as mocked:
            self._client.add_key('mocked-key', 'mocked-value')

            mocked.assert_called_once_with('mocked-key',
                                           'mocked-value',
                                           ttl=None)

    @attr('integration')
    def test_add_key_returns(self):
        result = self._client.add_key(self._key, 'value')
        time.sleep(self._sleep_time)

        self.assertEquals('value', result.value)

        self._client.delete_key(self._key)

    def test_watch_key(self):
        with patch('tribe.client.Client.get_key') as mocked:
            self._client.watch_key('mocked-key')

            mocked.assert_called_once_with('mocked-key',
                                           recursive=False,
                                           wait=True)

    @attr('integration')
    def test_watch_key_returns(self):
        self._client.add_key(self._key, 'value')
        time.sleep(self._sleep_time)

        queue = multiprocessing.Queue()

        def change_value(key, value):
            c = client.Client(self._config)
            c.add_key(key, value)

        def watch_value(key, queue):
            c = client.Client(self._config)
            queue.put(c.watch_key(key).value)

        watcher = multiprocessing.Process(target=watch_value,
                                          args=(self._key, queue))

        changer = multiprocessing.Process(target=change_value,
                                          args=(self._key, 'new-value',))

        watcher.start()
        changer.start()

        result = queue.get(timeout=2)
        watcher.join(timeout=5)
        changer.join(timeout=5)

        self.assertEquals('new-value', result)

    @attr('integration')
    def test_ping_returns(self):
        with patch('socket.getfqdn') as mocked:
            mocked.return_value = 'mocked-fqdn'
            result = self._client.ping()
            time.sleep(self._sleep_time)

            self.assertEquals(10, result.ttl)
            self.assertEquals('/tribe/nodes/mocked-fqdn', result.key)
            assert datetime.datetime.fromtimestamp(float(result.value))

            self._client.delete_key(result.key)
