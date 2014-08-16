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

from tribe import config


class TestConfig(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(__file__)
        f = os.path.join(basedir, 'test.json')
        self._config = config.Config(config_file=f)

    def test_connection_tuple_accessor(self):
        result = self._config.connection_tuple
        expected = (('192.168.20.13', 4001), ('192.168.20.14', 4001))

        self.assertEquals(expected, result)

    def test_etcd_path_accessor(self):
        result = self._config.etcd_path

        self.assertEquals('/tribe/nodes', result)

    def test_ping_ttl_accessor(self):
        result = self._config.ping_ttl

        self.assertEquals(10, result)
