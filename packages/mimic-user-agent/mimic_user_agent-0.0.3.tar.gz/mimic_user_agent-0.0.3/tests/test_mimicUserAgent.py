import unittest
from src.mimicUserAgent import mimic_user_agent as mua


class TestRandomUserAgent(unittest.TestCase):

    def test_not_None(self):
        self.assertEqual(type(mua()), str)

    def test_persistence(self):
        string = 'Mozilla/5.0 (Windows NT 10.0; x86; rv:107.0) Gecko/20100101 Firefox/107.0'
        self.assertEqual(mua(1), string)


if __name__ == '__main__':
    unittest.main()
