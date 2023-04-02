from requests.utils import get_encoding_from_headers
import unittest

class TestGetEncodingFromHeaders(unittest.TestCase):
    def test_get_encoding_from_headers_missing_content_type(self):
        headers = {}
        self.assertIsNone(get_encoding_from_headers(headers))
        
    def test_get_encoding_from_headers_explicit_charset(self):
        headers = {'content-type': 'text/html; charset=utf-8'}
        self.assertEqual(get_encoding_from_headers(headers), 'utf-8')
        
    def test_get_encoding_from_headers_implicit_charset(self):
        headers = {'content-type': 'text/html'}
        self.assertEqual(get_encoding_from_headers(headers), 'ISO-8859-1')
        
    def test_get_encoding_from_headers_json(self):
        headers = {'content-type': 'application/json'}
        self.assertEqual(get_encoding_from_headers(headers), 'utf-8')
        
    def test_get_encoding_from_headers_invalid_content_type(self):
        headers = {'content-type': 'invalid'}
        self.assertIsNone(get_encoding_from_headers(headers))
        
    def test_get_encoding_from_headers_none_headers(self):
        with self.assertRaises(AttributeError):
            get_encoding_from_headers(None)
