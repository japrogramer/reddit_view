#!/usr/bin/env python
from pprint import pprint
import sys, argparse, requests, json, time, re, itertools

PATTERNS = {}


class RedditLogic:
    request_headers = {'User-Agent': 'curl/7.24.0', 'Content-Type': 'application/json; charset=UTF-8'}
    combinations = []

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dispatch(self):
        self.combinations = self.combinatronics_of_params()
        urls = self.concat_urls()

    def concat_urls(self):
        urls = []
        for item in self.combinations:
            print(item)

    def form_urls(self, *args, **kwargs):
            # url = r'http://www.reddit.com/' + index + '/' + sec_index
            # tail = '/.json'+ '?limit=' + count
            # if order:
                # url += '/' + order
        # return url
        pass

    def get_json(self, data):

        pass

    def get_image_urls(self):
        pass

    def combinatronics_of_params(self):
        clean_subreddits = [x.strip() for x in self.subreddits.split(',')]
        clean_order = [x.strip() for x in self.order.split(',')]
        return list(itertools.product(
            self.index, self.clean_subreddits, self.clean_order, self.count))


def main():
    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument('-i', '--i', metavar='r', nargs='?', help='Index for subs', default='r', required=False)
    parser.add_argument('-s', '--s', metavar='funy,', nargs='?', help='comma seperated list of subreddits', default='funy,', required=False)
    parser.add_argument('-o', '--o', metavar='hot,top', nargs='?', help='comma seperated list of orders', default='hot,', required=False)
    parser.add_argument('-c', '--c', metavar='nnn', nargs='?', help='count of posts to consider', default='100', required=False)
    parser.add_argument('-p', '--p', metavar='nnn', nargs='?', help='count of points post must have', default='100', required=False)
    args = parser.parse_args()
    # return args
    reddit = RedditLogic(vars(args))
    reddit.dispatch()
    # print(set(urls), sep='\n')

entry = main
