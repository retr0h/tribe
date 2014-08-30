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

import itertools
import socket

import hash_ring


def _flatten_address_list(d):
    """
    Takes a dict of lists and flattens the values into a single list.
    Returns a list.
    """
    return list(itertools.chain(*d.values()))


def get_hostname():
    return socket.getfqdn()


def hash_addresses(servers, addresses):
    """
    Consistently hash `addresses` across a list of `servers`.  Returns a dict
    of {hostname => [IPv4 addresses the node manages]}.

    :param servers: A list of servers participating.
    :param addresses: A list of IPv4 addresses to be hashed against the
                      participating servers.
    """
    ring = hash_ring.HashRing(servers)
    addr_dict = {}
    for address in addresses:
        server = ring.get_node(address)
        addr_dict.setdefault(server, []).append(address)

    return addr_dict


def all_addresses(servers, addresses):
    """
    Returns a list of all the IPv4 addresses tribe is managing.
    """
    ha = hash_addresses(servers, addresses)

    return _flatten_address_list(ha)


def my_addresses(servers, addresses):
    """
    Returns a list of IPv4 addresses the node manages.
    """
    hostname = get_hostname()
    ha = hash_addresses(servers, addresses)

    return ha.get(hostname, [])


def not_my_addresses(servers, addresses):
    """
    Returns a list of IPv4 addresses the node does not manage.
    """
    hostname = get_hostname()
    ha = hash_addresses(servers, addresses)
    ha.pop(hostname, [])

    return _flatten_address_list(ha)
