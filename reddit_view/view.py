#!/usr/bin/env python
from pprint import pprint
import sys, argparse, requests, json, time, re, itertools

PATTERNS = {
    'gallery':  (lambda x: re.compile(".+\/(a|gallery|gfycat)\/.+$").match(x)),
    'comments': (lambda x:  re.compile(".+\/comments\/.+$").match(x)),
    'ext':  (lambda x:  re.compile("^.+\.(jpg|png|jpeg|gif)(.+)?$").match(x)),
    'imgur':  (lambda  x: re.compile(".+\/imgur\/.+$").match(x)),
    'not_img': (lambda  x:  re.compile(".+(video|html|\/)(.+)?$").match(x)),}


class RedditLogic:
    request_headers = {'User-Agent': 'curl/7.24.0', 'Content-Type': 'application/json; charset=UTF-8'}
    combinations = []

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dispatch(self):
        self.combinations = self.combinatronics_of_params()
        self.urls = self.concat_urls()
        self.urls_to_filter = self.get_image_urls()
        return set(self.match_pattern())

    def match_pattern(self):
        clean_urls =[]
        for url in self.urls_to_filter:
            if (not PATTERNS['gallery'](url)) and (not PATTERNS['comments'](url)):
                if (PATTERNS['ext'](url)):
                    clean_urls.append(url)
                elif not PATTERNS['not_img'](url):
                    merged = imgur_link + '.jpg'
                    clean_urls.append(merged)

        return clean_urls


    def extract_image_url(self, data):
        links = []
        for child in data['data']['children']:
            score = child['data']['score']
            if int(score) >= int(self.p):
                links.append(child['data']['url'])
        return links

    def get_json(self, url):
        r = requests.get(url, headers=self.request_headers)
        return r.json()

    def get_image_urls(self):
        image_urls = []
        for url in self.urls:
            data = self.get_json(url)
            try:
                image_urls += self.extract_image_url(data)
            except KeyError as error:
                print(error)
        return image_urls

    def form_urls(self, index, subreddit, order, count):
        url = r'http://www.reddit.com/' + index + '/' + subreddit
        tail = '/.json'+ '?limit=' + count
        url += '/' + order
        url += tail
        return url

    def concat_urls(self):
        urls = []
        for item in self.combinations:
            urls.append(self.form_urls(*item))
        return urls

    def combinatronics_of_params(self):
        clean_subreddits = [x.strip() for x in self.s.split(',')]
        clean_subreddits = filter(None, clean_subreddits)
        clean_order = [x.strip() for x in self.o.split(',')]
        clean_order = filter(None, clean_order)
        return list(itertools.product( self.i, clean_subreddits, clean_order, [self.c,]))

def set_up_parser():
    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument('-i', '--i', metavar='r', nargs='?', help='Index for subs', default='r', required=False)
    parser.add_argument('-s', '--s', metavar='funy,', nargs='?', help='comma seperated list of subreddits', default='funy,', required=False)
    parser.add_argument('-o', '--o', metavar='hot,top', nargs='?', help='comma seperated list of orders', default='hot,', required=False)
    parser.add_argument('-c', '--c', metavar='nnn', nargs='?', help='count of posts to consider', default='100', required=False)
    parser.add_argument('-p', '--p', metavar='nnn', nargs='?', help='count of points post must have', default='100', required=False)
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
