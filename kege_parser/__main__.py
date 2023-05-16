TITLE_MSG = """
    __ __ __________________
   / //_// ____/ ____/ ____/___  ____ ______________  _____
  / ,<  / __/ / / __/ __/ / __ \/ __ `/ ___/ ___/ _ \/ ___/
 / /| |/ /___/ /_/ / /___/ /_/ / /_/ / /  (__  )  __/ /
/_/ |_/_____/\____/_____/ .___/\__,_/_/  /____/\___/_/
                       /_/

by Butukay <butukay@gmail.com>
""".strip("\n") + "\n"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    '-q', '--quiet', dest='quiet', action="store_true", help='be quiet as possible (no logs)')

subparsers = parser.add_subparsers(dest='subparser')

parser_download = subparsers.add_parser('download')
parser_download.add_argument(
    "test_id", type=int)

parser_answers = subparsers.add_parser('answers')
parser_answers.add_argument(
    "test_id", type=int)
parser_answers.add_argument(
    '-j', '--json', dest='rjson', action="store_true", help='Return answers in json format')

parser_run = subparsers.add_parser('run')
parser_run.add_argument(
    "test_id", type=int)
parser_run.add_argument(
    '-t', '--test', dest='test', action="store_true", help='compare execution results with downloaded answers')
parser_run.add_argument(
    '-m', '--my-answers', dest='my_answers', action="store_true", help='show execution result answers')
parser_run.add_argument(
    '-r', '--right-answers', dest='right_answers', action="store_true", help='show right answers')
parser_run.add_argument(
    '--time-limit', dest='time_limit', type=int, default=20, help='execution time limit in seconds')

from kege_parser.commands import *

def main():
    args = parser.parse_args()

    if not args.quiet:
        print(TITLE_MSG)

    if not args.subparser:
        return print("Nothing to do")

    kwargs = vars(args)
    return globals()[kwargs.pop('subparser')](**kwargs)


import sys
if __name__ == "__main__":
    sys.exit(
        main()
    )
