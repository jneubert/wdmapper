# -*- coding: utf-8 -*-
"""Wraps wdmapper as command line client."""

from __future__ import unicode_literals, print_function
import argparse
import sys

import wdmapper
from .exceptions import WdmapperError


def parse_args(argv):
    """parse wdmapper command line arguments."""

    parser = argparse.ArgumentParser(
        prog='wdmapper',
        description="Manage Wikidata authority file mappings.",
        epilog="See <https://github.com/gbv/wdmapper#readme> for details."
    )

    parser.add_argument('-f', '--from', metavar='NAME',
                        help='input format (default: csv)')
    parser.add_argument('-t', '--to', metavar='NAME',
                        help='output format (default: beacon)')
    parser.add_argument('-i', '--input', default='-', metavar='IN',
                        help='input file to read from (default: - for STDIN)')
    parser.add_argument('-o', '--output', default='-', metavar='OUT',
                        help='output file to write to (default: - for STDOUT)')
    parser.add_argument('-s', '--sort', action='store_true',
                        help='sort mappings for normalized output')
    parser.add_argument('-l', '--limit', metavar='N', type=int, default=0,
                        help='maximum number of mappings to process')
    parser.add_argument('-H', '--no-header', dest='no_header', action='store_true',
                        help='read/write CSV/BEACON without header')
    parser.add_argument('-C', '--no-cache', dest='cache',
                        action='store_false', default=True,
                        help='disable caching')
    parser.add_argument('-r', '--relation', metavar='R',
                        help='mapping relation URI such as skos:exactMatch or owl:sameAs')
    parser.add_argument('-n', '--dry-run', dest='dry', action='store_true',
                        help='don\'t perform any edits on Wikidata')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug mode')
    parser.add_argument('-V', '--version', action='store_true',
                        help='show version number of this script')

    parser.add_argument('command', nargs='?',
                        help=', '.join(wdmapper.commands))
    parser.add_argument('source', nargs='?',
                        help='source property given by id, URL, URI, or label')
    parser.add_argument('target', nargs='?',
                        help='target property given by id, URL, URI, or label')

    args = parser.parse_args(argv)

    if args.command == 'help':
        parser.print_help()
        sys.exit(0)

    if args.version:
        print('wdmapper %s' % wdmapper.__version__)
        sys.exit(0)

    command = args.command
    del args.command

    if args.target is None:
        if command is not None and command not in wdmapper.commands:
            if args.source is None:
                args.target = command
            else:
                args.target = args.source
                args.source = command
            command = 'head'
        else:
            args.target = args.source
            args.source = None

    if command is None:
        command = 'convert'

    return command, args


def run(*args):
    """Execute wdmapper from module with list of command line arguments."""

    try:
        command, args = parse_args(list(args))
        wdmapper.wdmapper(command, **vars(args))
    except WdmapperError as e:
        print(e.message(), file=sys.stderr)
        sys.exit(1)


def main():
    """Run wdmapper from command line.

    Command line arguments are taken from ``sys.argv`` and decoded to Unicode.
    """

    encoding = sys.stdout.encoding or 'utf-8'
    args = map(lambda arg: arg.decode(encoding), sys.argv[1:])
    run(*args)
