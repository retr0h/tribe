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


class Agent(object):
    """
    Manages IP addresses on the node running the agent.  Currently only
    supports IPv4 addresses realized as IP aliases on the configured interface.

    An agents workflow:
      1. Start the agent's loop.
      2. Begin watching `config.etcd_path` for changes.
        - Currently keys are added to this directory by cron job executing
          `tribe --ping`.
        - Keys are added with a configurable TTL.
        - Allow etcd to expire keys which have not been updated before the
          TTL expires.  We assume this is a server failure and re-hash IPs.
      3. On change use consistent hashing to map IP(s) to node running agent.

    TODO(retr0h): prevent race condition on watch.
    """
    def __init__(self, config):
        self._client = client.Client()
        self._etcd_path = config.etcd_path
        self._sleep_interval = config.sleep_interval

    def _watch(self):
        """
        Blocking call to watch the `etcd_path` for changes.  Returns a list of
        etcd.EtcdResult objects.
        """
        self._watch_key(self._etcd_path, recursive=True)

    def run(self):
        while True:
            time.sleep(self._sleep_interval)
