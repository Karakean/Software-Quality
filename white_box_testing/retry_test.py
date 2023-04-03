import unittest
from unittest.mock import Mock, patch
import requests

class TestRequestRetry(unittest.TestCase):
    @patch('requests.get')
    def test_first_request_succeeds(self, mock_get):
        mock_get.return_value.status_code = 200
        url = "http://localhost:8080"
        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_first_request_times_out(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        url = "http://localhost:8080"
        with self.assertRaises(requests.exceptions.Timeout):
            requests.get(url, timeout=1)

    @patch('requests.get')
    def test_second_request_succeeds(self, mock_get):
        mock_response = Mock(status_code=200)
        mock_get.side_effect = [requests.exceptions.Timeout, mock_response]
        url = "http://localhost:8080"
        try:
            response = requests.get(url, timeout=1)
        except requests.exceptions.Timeout:
            pass
        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_both_requests_time_out(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        url = "http://localhost:8080"
        with self.assertRaises(requests.exceptions.Timeout):
            requests.get(url, timeout=1)
        with self.assertRaises(requests.exceptions.Timeout):
            requests.get(url, timeout=0.5)
