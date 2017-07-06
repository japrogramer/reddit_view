from unittest.mock import patch, PropertyMock
from reddit_view import view

import unittest
import json


class TestRedditLogic(unittest.TestCase):

    def setUp(self):
        self.initial = {
                'i': 'r',
                's': 'pics,',
                'o': 'hot,new,top',
                'p': '100',
                'c': '100'}

    def test_kwargs_in_self(self):
        reddit = view.RedditLogic(**self.initial)
        for attribute in self.initial:
            self.assertIn(attribute, dir(reddit))
        with patch.dict(self.initial, {'test1': 'value'}, clear=True):
            fake = view.RedditLogic(**self.initial)
            for attribute in self.initial:
                self.assertIn(attribute, dir(fake))

    @patch('reddit_view.view.RedditLogic.get_json')
    def test_dispatch(self, MockReddit):
        url = 'it works.jpg'
        data = {'data':
                {'children':
                    [
                        {'data': {'score': 9000, 'url': url, }, },
                    ], }, }

        MockReddit.return_value = data
        reddit = view.RedditLogic(**self.initial)
        assert MockReddit is view.RedditLogic.get_json
        assert MockReddit.called_called_with(**self.initial)
        test_value = reddit.dispatch()
        self.assertEqual(test_value, set([url, ]))

    def test_match_pattern(self):
        good = [
                '/this.jpg']
        bad = [
                '/comments/',
                '/a/',
                '/gallery/',
                '/video/',
                '/html/',
                '/', ]

        value = sorted(good + bad)

        with patch(
                'reddit_view.view.RedditLogic.urls_to_filter',
                new_callable=PropertyMock) \
                as mock_foo:

            mock_foo.return_value = value
            reddit = view.RedditLogic(**self.initial)
            self.assertEqual(reddit.urls_to_filter, value)
            clean = reddit.match_pattern()
            self.assertNotIn(bad, clean)

    @patch('reddit_view.view.RedditLogic.get_json')
    def test_extract_image_url(self, MockReddit):
        return True
        # TODO test gets url
        url = 'it works.jpg'
        data = {
              "data": {
                "children": {
                  "data": {
                    "url": url,
                    "score": 5,
                  }
                },
              }
            }

        import json
        data = json.dumps(data)

        MockReddit.return_value = data
        reddit = view.RedditLogic(**self.initial)
        test_value = reddit.dispatch()
        self.assertEqual(test_value, [ url ])

    @patch('reddit_view.view.requests.get')
    def test_get_json(self, MockRequests):
        mock_json = unittest.mock.Mock(side_effect=KeyError('foo'))
        MockRequests.return_value = mock_json
        reddit = view.RedditLogic(**self.initial)
        reddit.get_json('http://test')
        self.assertTrue(mock_json.json.called)


class TestImgurGallery(unittest.TestCase):

    def setUp(self):
        self.path = 'google.com'

    @patch('view.requests.get')
    def test_gen_list(self, mock_get):
        mock_get.side_effect = [ unittest.mock.MagicMock(status_code=200, content='<html></html>') ]

        img_class = view.ImgurGallery(**{'url': self.path})
        value = img_class.dispatch()
        self.assertEqual(img_class.page.content, '<html></html>')
        self.assertEqual(value, [])



if __name__ == '__main__':
        unittest.main()
