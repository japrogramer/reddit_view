import unittest
from reddit_view import view


class TestRedditLogic(unittest.TestCase):

    def setUp(self):
        self.argvs = vars(view.set_up_parser())
        pass

    def test_kwargs_in_self(self):
        # reddit = view.RedditLogic(argvs)
        # self.assertIn(argvs, reddit.__dict__)
        pass


if __name__ == '__main__':
        unittest.main()
