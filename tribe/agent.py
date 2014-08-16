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
from tribe import config
from tribe import util


class Agent(object):
    """
    Manages IP addresses on the node running the agent.  Currently only
    supports IPv4 addresses realized as IP aliases on the configured interface.

    An agents workflow:
      1. Start the agent's loop.
      2. Begin watching /tribe/nodes/ for changes.
      3. On change use consistent hashing to map IP(s) to node running agent.

    TODO(retr0h): prevent race condition on watch.
    """
    def __init__(self):
        self._client = client.Client()
        self._etcd_path = config.Config().etcd_path
        self._sleep_interval = 3
        self._node_ttl = 5

    def _ping(self):
        """
        add itself with a low ttl to
          /tribe/nodes/$hostname: time.time()
        """
        path = '{prefix}/{hostname}'.format(prefix=self._etcd_path,
                                            hostname=util.get_hostname())
        self._client.write(path, time.time(), ttl=self._node_ttl)

    def _watch(self):
        """
        Blocking...
        """
        self._watch_key(self._etcd_path, recursive=True)

    def run(self):
        while True:
            time.sleep(self._sleep_interval)
