import unittest
import requests

class TestGoogleCookies(unittest.TestCase):
    def test_cookie_count(self):
        r = requests.get('https://google.com')
        self.assertEqual(len(r.cookies), 3)

    def test_pop_cookie(self):
        r = requests.get('https://google.com')
        init_cookie_count = len(r.cookies)
        r.cookies.popitem()
        self.assertEqual(len(r.cookies), init_cookie_count - 1)

if __name__ == '__main__':
    unittest.main()
