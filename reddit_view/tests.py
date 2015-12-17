import unittest
from reddit_view import view


class TestRedditLogic(unittest.TestCase):

    def setUp(self):
        self.initial = {
                'i': 'r',
                's': 'test,another,',
                'o': 'hot,new,top',
                'p': '100',
                'c': '100'}

    def test_kwargs_in_self(self):
        reddit = view.RedditLogic(self.initial)
        self.assertIn(dir(self.initial), dir(reddit))
        pass


if __name__ == '__main__':
        unittest.main()
