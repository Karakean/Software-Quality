import unittest
from requests.utils import parse_header_links

class TestParseHeaderLinks(unittest.TestCase):
    def test_parse_header_links(self):
        link_header = '<https://api.example.com/page/1>; rel="prev", <https://api.example.com/page/3>; rel="next"'
        expected_links = {'prev': 'https://api.example.com/page/1', 'next': 'https://api.example.com/page/3'}
        links = parse_header_links(link_header)
        self.assertDictEqual(links, expected_links)

    def test_parse_header_links_missing_links(self):
        link_header = ''
        expected_links = {}
        links = parse_header_links(link_header)
        self.assertDictEqual(links, expected_links)

    def test_parse_header_links_invalid_links(self):
        link_header = '<https://api.example.com/page/1> rel="prev"'
        expected_links = {}
        links = parse_header_links(link_header)
        self.assertDictEqual(links, expected_links)