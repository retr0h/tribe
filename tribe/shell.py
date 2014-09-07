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
    ap.add_argument('--cleanup', action='store_true',
                    help='Cleanup aliases on the host.')
    args = vars(ap.parse_args())
    return args


def main():
    args = _parse_args()
    conf = config.Config()
    c = client.Client(conf)
    a = agent.Agent(conf)

    if args['ping']:
        c.ping()
    elif args['agent']:
        a.run()
    # TODO(retr0h): Not sure I like this under agent anylonger.
    elif args['cleanup']:
        a.cleanup()

if __name__ == '__main__':
    main()
