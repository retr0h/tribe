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

import time

from tribe import client
from tribe import util


class Agent(object):
    """
    Tribe Agent

    agent
      - start loop
      - create base nodes with low ttl
      - ping
          - add itself with a low ttl
            /tribe/nodes/$hostname: time.time()
      - watch /tribe/nodes/
    """
    def __init__(self):
        self._client = client.Client()
        self._sleep_interval = 3
        self._node_ttl = 5

    def _ping(self):
        path = '/tribe/nodes/{0}'.format(util.get_hostname())
        self._client.write(path, time.time(), ttl=self._node_ttl)

    def _watch(self):
        """
        Blocking...
        """
        path = '/tribe/nodes'
        self._watch_key(path, recursive=True)
        result = self._get_key(path, recursive=True)
        print [subkey.key for subkey in result.children]

    def run(self):
        while True:
            time.sleep(self._sleep_interval)
