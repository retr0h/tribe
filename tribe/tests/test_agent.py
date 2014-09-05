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

import unittest2 as unittest
from mock import patch

from tribe import agent
from tribe import config


class TestClient(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(__file__)
        f = os.path.join(basedir, 'support', 'test.json')
        self._config = config.Config(config_file=f)
        self._agent = agent.Agent(self._config)

    def test_cleanup(self):
        with patch('tribe.util.get_other_addresses') as mocked:
            mocked.return_value = ['2.2.2.2']
            with patch('tribe.util.delete_alias') as mocked_cmd:
                self._agent._cleanup()

                mocked_cmd.assert_called_once_with('2.2.2.2',
                                                   'eth0')

    def test_setup(self):
        with patch('tribe.util.get_own_addresses') as mocked:
            mocked.return_value = ['1.1.1.1']
            with patch('tribe.util.add_alias') as mocked_cmd:
                self._agent._setup()

                mocked_cmd.assert_called_once_with('1.1.1.1',
                                                   'eth0')
