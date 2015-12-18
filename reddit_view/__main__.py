from .view import RedditLogic

import argparse


def set_up_parser():
    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument(
            '-i', '--i',
            metavar='r', nargs='?',
            help='Index for subs', default='r', required=False)

    parser.add_argument(
            '-s', '--s',
            metavar='funy,', nargs='?',
            help='comma seperated list of subreddits',
            default='funy,', required=False)

    parser.add_argument(
            '-o', '--o',
            metavar='hot,top', nargs='?',
            help='comma seperated list of orders',
            default='hot,', required=False)

    parser.add_argument(
            '-c', '--c',
            metavar='nnn', nargs='?',
            help='count of posts to consider',
            default='100', required=False)

    parser.add_argument(
            '-p', '--p',
            metavar='nnn', nargs='?',
            help='count of points post must have',
            default='100', required=False)

    args = parser.parse_args()
    return args


def main():
    # return args
    args = set_up_parser()
    reddit = RedditLogic(**vars(args))
    show = reddit.dispatch()
    print(*show, sep='\n')

if __name__ == "__main__":
    main()
