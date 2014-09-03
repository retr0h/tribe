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

"""
Tribe CLI tool.
"""

import argparse

import tribe
from tribe import agent
from tribe import client
from tribe import config


def _parse_args():
    ap = argparse.ArgumentParser(prog='tribe',
                                 description=__doc__.strip())
    ap.add_argument('--version', action='version',
                    version=tribe.__version__)
    ap.add_argument('--ping', action='store_true',
                    help='Ping the `etcd_path`.')
    ap.add_argument('--agent', action='store_true',
                    help='Start the agent.')
    args = vars(ap.parse_args())
    return args


if __name__ == '__main__':
    args = _parse_args()
    c = config.Config()

    if args['ping']:
        client.Client(c).ping()
    elif args['agent']:
        agent.Agent(c).run()
