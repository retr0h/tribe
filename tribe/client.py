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

import etcd


class Client(object):
    """
    A client which handles interactions with etcd.
    """

    def __init__(self, ct=None):
        # TODO(retr0h): Move this elsewhere.
        if not ct:
            ct = (('192.168.20.13', 4001), ('192.168.20.14', 4001))
        self._client = etcd.Client(ct)

    def get_key(self, key, recursive=False, wait=False):
        """
        Fetch the given `key`.  Returns a list of etcd.EtcdResult objects
        when `recursive` is True, otherwise an etcd.EtcdResult object.

        :param key: A string with the key to fetch.
        :param recursive: A bool to recursively fetch a dir.
        :param wait: A bool if to wait and return next time the `key` changes.
        """
        result = self._client.read(key, recursive=recursive, wait=wait)
        if not result.dir:
            return result
        else:
            # NOTE(retr0h): Not sure using _children is a good idea.
            return [subkey for subkey in result.children
                    if len(result._children) > 0]

    def add_key(self, key, value, ttl=None):
        return self._client.set(key, value, ttl=ttl)

    def delete_key(self, key):
        return self._client.delete(key)

    def watch_key(self, key, recursive=False):
        return self.get_key(key, recursive=recursive, wait=True)
