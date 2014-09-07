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

import os
import time

import unittest2 as unittest
from mock import patch
from nose.plugins.attrib import attr

from tribe import agent
from tribe import client
from tribe import config


class TestClient(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(__file__)
        f = os.path.join(basedir, 'support', 'test.json')
        self._config = config.Config(config_file=f)
        self._agent = agent.Agent(self._config)
        self._client = client.Client(self._config)

    @attr('integration')
    def test_get_servers(self):
        keys = ['/tribe/nodes/mocked-1.example.com',
                '/tribe/nodes/mocked-2.example.com',
                '/tribe/nodes/mocked-3.example.com']
        for key in keys:
            self._client.add_key(key, 'value')
        time.sleep(0.1)

        result = self._agent._get_servers()
        self.assertEquals(3, len(result))
        self.assertEquals('mocked-1.example.com', result[0])

        for key in keys:
            self._client.delete_key(key)

    @patch('tribe.agent.Agent._get_servers')
    @patch('tribe.util.get_other_addresses')
    @patch('tribe.util.delete_alias')
    def test_cleanup(self, mocked_cmd, mocked_addresses, mocked_servers):
        mocked_servers.return_value = ['mocked-1.example.com',
                                       'mocked-2.example.com',
                                       'mocked-3.example.com']
        mocked_addresses.return_value = ['2.2.2.2']
        self._agent.cleanup()

        mocked_cmd.assert_called_once_with('2.2.2.2',
                                           'eth0')

    @patch('tribe.agent.Agent._get_servers')
    @patch('tribe.util.get_own_addresses')
    @patch('tribe.util.add_alias')
    def test_setup(self, mocked_cmd, mocked_addresses, mocked_servers):
        mocked_servers.return_value = ['mocked-1.example.com',
                                       'mocked-2.example.com',
                                       'mocked-3.example.com']
        mocked_addresses.return_value = ['1.1.1.1']
        self._agent._setup()

        mocked_cmd.assert_called_once_with('1.1.1.1',
                                           'eth0')
