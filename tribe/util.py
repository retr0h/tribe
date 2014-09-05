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
import os
import socket
import subprocess

import hash_ring
import netifaces


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


def get_own_addresses(servers, addresses):
    """
    Returns a list of IPv4 addresses the node manages.
    """
    hostname = get_hostname()
    ha = hash_addresses(servers, addresses)

    return ha.get(hostname, [])


def get_other_addresses(servers, addresses):
    """
    Returns a list of IPv4 addresses the node does not manage.
    """
    hostname = get_hostname()
    ha = hash_addresses(servers, addresses)
    ha.pop(hostname, [])

    return list(itertools.chain(*ha.values()))


def _handle_result(exitcode, err):
    """
    Checks the exitcode for success.  If successful returns True,
    otherwise raises on failure.

    :param exitcode: An int containing the command's exit status.
    :param err: A string containing the command's STDERR.
    :raises: Exception when command failed.
    """
    if exitcode == 0:
        return True
    else:
        raise Exception(err)


def execute(command):
    """
    Executes a command in a subprocess.  Returns the result of
    `_handle_result()`.

    :param command: Command string to execute.
    """
    process = subprocess.Popen(command,
                               cwd=os.getcwd(),
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    (out, err) = process.communicate()
    exitcode = process.wait()

    return _handle_result(exitcode, err)


def add_alias(ip, interface, label):
    if not get_alias(label):
        cmd = ('sudo ip addr add {ip} '
               'dev {interface} '
               'label {label}').format(**locals())

        execute(cmd)


def delete_alias(ip, interface, label):
    if not get_alias(label):
        cmd = ('sudo ip addr del {ip} '
               'dev {interface} '
               'label {label}').format(**locals())

        execute(cmd)


def get_alias(interface):
    """
    Determine if the given interface exists.  Aliases added with a label appear
    as a separate interface by `netifaces`.  Returns True if the interface
    exists otherwise False.

    :param interface: A string with the interface to find.
    """
    try:
        netifaces.ifaddresses(interface)
        return True
    except ValueError:
        return False
