#!/usr/bin/env python
import sys, requests, json, re, itertools, time, pprint

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

PATTERNS = {
    'gallery':  (lambda x: re.compile(".+\/(a|gallery|gfycat)\/.+$").match(x)),
    'comments': (lambda x: re.compile(".+\/comments\/.+$").match(x)),
    'ext':  (lambda x: re.compile("^.+\.(jpg|png|jpeg|gif)(.+)?$").match(x)),
    'imgur':  (lambda x: re.compile(".+\/imgur\/.+$").match(x)),
    'not_img': (lambda x: re.compile(".+(video|html|\/)(.+)?$").match(x)),
    }

ua = UserAgent()
request_headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        }


class RedditLogic:

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
            elif PATTERNS['gallery'](url):
                gallery = ImgurGallery(**{'url': url})
                gallery_list = gallery.dispatch()
                clean_urls.extend(gallery_list)


        return clean_urls

    def extract_image_url(self, data):
        links = []
        for child in data['data']['children']:
            score = child['data']['score']
            if int(score) >= int(self.p):
                links.append(child['data']['url'])
        return links

    def get_json(self, url):
        r = requests.get(url, headers=request_headers)
        # r = requests.get(url)
        return r.json()

    def get_image_urls(self):
        image_urls = []
        count = 0
        wait = 3
        for url in self.urls:
            data = self.get_json(url)
            count += 1
            try:
                start = time.time() + wait
                time.sleep(wait)
                image_urls += self.extract_image_url(data)
                elapsed = start - time.time()
            except KeyError as error:
                eprint('error \n')
                eprint('url: ', url)
                eprint(data)
        return image_urls

    def form_urls(self, index, subreddit, order, count):
        url = r'http://www.reddit.com/' + index + '/' + subreddit
        url += '/' + order

        tail = '/.json' + '?limit=' + count
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
        return list(itertools.product(
                    self.i,
                    clean_subreddits,
                    clean_order,
                    [self.c, ]))


class ImgurGallery:

    page = None

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def dispatch(self):
        self.get_page()
        return self.get_gallery()

    def get_page(self):
        try:
            self.page = requests.get(self.url, headers=request_headers)
        except:
            raise Exception('spam', 'eggs')
        return

    def get_gallery(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        container = soup.find('div', {'class': 'post-images'})
        if container:
            a_src = ['http:' + img.get('src') for img in container.find_all('img')]
            return a_src
        return []
