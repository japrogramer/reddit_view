#!/usr/bin/env python
import requests
import json
import re
import itertools
import time

PATTERNS = {
    'gallery':  (lambda x: re.compile(".+\/(a|gallery|gfycat)\/.+$").match(x)),
    'comments': (lambda x: re.compile(".+\/comments\/.+$").match(x)),
    'ext':  (lambda x: re.compile("^.+\.(jpg|png|jpeg|gif)(.+)?$").match(x)),
    'imgur':  (lambda x: re.compile(".+\/imgur\/.+$").match(x)),
    'not_img': (lambda x: re.compile(".+(video|html|\/)(.+)?$").match(x)),
    }


class RedditLogic:
    request_headers = {
            'User-Agent': 'curl/7.24.0',
            'Content-Type': 'application/json; charset=UTF-8'}
    combinations = []
    urls = []
    urls_to_filter = []

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def dispatch(self):
        self.combinations = self.combinatronics_of_params()
        self.urls = self.concat_urls()
        self.urls_to_filter = self.get_image_urls()
        return set(self.match_pattern())

    def match_pattern(self):
        clean_urls = []
        for url in self.urls_to_filter:
            if (not PATTERNS['gallery'](url)) and \
                    (not PATTERNS['comments'](url)):
                if (PATTERNS['ext'](url)):
                    clean_urls.append(url)
                elif not PATTERNS['not_img'](url):
                    merged = url + '.jpg'
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
        count = 0
        elapsed = 0
        wait = 3
        for url in self.urls:
            data = self.get_json(url)
            count += 1
            try:
                start = time.time()
                if elapsed < wait:
                    time.sleep(wait)
                image_urls += self.extract_image_url(data)
                elapsed = start - time.time()
            except KeyError as error:
                print(count)
                print(data)
                raise error
        return image_urls

    def form_urls(self, index, subreddit, order, count):
        url = r'http://www.reddit.com/' + index + '/' + subreddit
        tail = '/.json' + '?limit=' + count
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
        return list(
                itertools.product(
                    self.i,
                    clean_subreddits,
                    clean_order,
                    [self.c, ]))
