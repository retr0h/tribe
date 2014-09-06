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

import json


class Config(object):
    """
    A class which handles the configuration of tribe.
    """

    def __init__(self, **kwargs):
        config_file = kwargs.get('config_file', '/etc/tribe.json')
        self._config = self._get_config(config_file)

    def _get_config(self, config_file):
        return json.load(open(config_file))

    @property
    def connection_tuple(self):
        """
        Create a connection object for `etcd.Client`.  Returns a tuple
        consisting of tuples in the form of (host, port).
        """
        hosts = self._config.get('etcd_hosts')
        port = self._config.get('etcd_port', 4001)
        return tuple([tuple([host, port]) for host in hosts])

    @property
    def etcd_path(self):
        return self._config.get('etcd_prefix', '/tribe/nodes')

    @property
    def ping_ttl(self):
        return self._config.get('ping_ttl', 10)

    @property
    def aliases(self):
        return self._config.get('aliases', [])

    @property
    def interface(self):
        return self._config.get('interface', 'eth0')
