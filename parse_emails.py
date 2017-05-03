#!/usr/bin/python
import argparse
import glob

import pprint
from collections import Counter

import os

from parsers import get_task_path_and_exc, get_task_args_and_kwargs
from argparse_types import readable_dir


def main():
    parser = argparse.ArgumentParser(
        description='A simple script to parse celery failure emails. The basic '
                    'idea is that Celery generates lots of error emails, so to '
                    'work with them, we parse them and generate code that we '
                    'can use to re-run the tasks. The error emails are created '
                    'as .eml files in Thunderbird and saved to a directory '
                    'that this program parses.')
    parser.add_argument(
        '--directory',
        type=readable_dir,
        help='The directory where we parse error emails. Use full paths.'
    )
    parser.add_argument(
        '--no-stats',
        default=False,
        action='store_true',
        help="Supress printing stats.",
    )
    cli_args = parser.parse_args()
    file_names = glob.glob(os.path.join(cli_args.directory, '*.eml'))
    print("There are %s files to parse." % len(file_names))
    task_name_stats = Counter()
    exception_stats = Counter()
    for file_name in file_names:
        print("Doing %s" % file_name)
        task_name, exc = get_task_path_and_exc(file_name)
        args, kwargs = get_task_args_and_kwargs(file_name)
        print("  Task %s with args %s and kwargs %s failed with %s" % (
            task_name,
            args,
            kwargs,
            exc,
        ))
        task_name_stats[task_name] += 1
        exception_stats[exc.split('(', 1)[0]] += 1

    if not cli_args.no_stats:
        pprint.pprint(task_name_stats)
        pprint.pprint(exception_stats)


if __name__ == '__main__':
    main()
