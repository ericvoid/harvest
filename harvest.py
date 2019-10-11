#!/usr/bin/env python3
import os
import sys

from collections import defaultdict
from glob import glob
from itertools import chain
from operator import itemgetter


SCRIPT_NAME = os.path.basename(__file__)


def harvest(source: str, extensions:list=[], glob_sort='alpha', paths_only=False):
    if os.path.isfile(source):
        if paths_only:
            yield source + os.linesep

        else:
            yield read_file(source)

    else:
        paths = glob(source + '/**/*', recursive=True)
        filtered_paths = filter(lambda path: has_extension(path, extensions) and os.path.isfile(path), paths)
        sorted_paths = _sort_glob_result(filtered_paths, glob_sort)

        if paths_only:
            yield from (path + os.linesep for path in sorted_paths)

        else:
            yield from map(read_file, sorted_paths)


def has_extension(path, extensions):
    return any(path.endswith(extension) for extension in extensions) if extensions else True


def _sort_glob_result(paths, glob_sort):
    if glob_sort == 'alpha':
        return sorted(paths)

    elif glob_sort == 'shallowfirst':
        return sorted(sorted(paths), key=lambda x: len(x.split(os.sep)))

    elif glob_sort == 'depthfirst':
        return _sort_deep_first([(path, path.split(os.sep)) for path in paths])

    else:
        raise ValueError('unknown glob sort order')


def _sort_deep_first(paths):
    # yield sorted directories
    directory_groups = defaultdict(list)

    for path, splitted in paths:
        if len(splitted) > 1:
            root = splitted[0]
            tail = splitted[1:]
            directory_groups[root].append((path, tail))

    for root, group in sorted(directory_groups.items(), key=itemgetter(0)):
        yield from _sort_deep_first(group)

    # yield sorted files
    files = (path for path, splitted in paths if len(splitted) == 1)

    for file in sorted(files):
        yield file


def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()

    except UnicodeDecodeError:
        print(f'{SCRIPT_NAME}: warning: could not read file {path}' , file=sys.stderr)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Harversts files in one or more directory trees and writes "
                    "all the content to stdout.",
        epilog="""
Multiple extensions can be provided by repeating the '-e'
extension argument (eg. '-e .txt -e .readme').

By default the files are sorted using alphabetial order. To sort 
them by depth use --depth-first or --shallow-first arguments.
""",
        )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--depth-first', action='store_true',
                       help="sorts the files so the deeper paths comes before the shallow "
                            "ones, and directories comes before the files (following the "
                            "pattern used by most file managers and IDEs)")
    group.add_argument('-s', '--shallow-first', action='store_true',
                       help="sorts the files so the shallow paths comes before the deep "
                            "ones (the opposite of --depth-first")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="display errors (errors are written to stderr)")

    parser.add_argument('-e', '--extension', action='append',
                        help="set a file extension to consider")

    parser.add_argument('-p', '--paths-only', action='store_true',
                        help="write only the file paths to stdout")

    parser.add_argument('source', nargs='+',
                        help="path to harvest content")

    args = parser.parse_args()

    try:
        extensions = args.extension or []

        sort_order = 'alpha'

        if args.depth_first:
            sort_order = 'depthfirst'

        elif args.shallow_first:
            sort_order = 'shallowfirst'

        for source in args.source:
            result = harvest(source, extensions, sort_order, args.paths_only)
            print(''.join(result), end='')

    except Exception:
        parser.print_usage(sys.stderr)
        if args.verbose:
            print(f'{SCRIPT_NAME}: error: unhandled exception', file=sys.stderr)

            import traceback
            traceback.print_exc()

        else:
            print(f'{SCRIPT_NAME}: error: unhandled exception (use --verbose argument to show error details)', file=sys.stderr)

        sys.exit(1)
