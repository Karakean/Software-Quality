import socket
import threading
import requests
import unittest
from urllib3.util import Timeout as TimeoutSauce
from wrapt_timeout_decorator import *


class SendTest(unittest.TestCase):

    @staticmethod
    def handle_requests(created_server):
        while True:
            client_socket, _ = created_server.accept()
            request_data = b''
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                request_data += chunk

    @staticmethod
    def create_non_responding_server():
        created_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        created_server.bind(('localhost', 0))
        created_server.listen()
        created_server_port = created_server.getsockname()[1]
        server_thread = threading.Thread(target=SendTest.handle_requests, args=(created_server,))
        server_thread.start()
        return f'http://localhost:{created_server_port}'

    @staticmethod
    def data_chunked():
        data = [b'hello', b'world']
        for chunk in data:
            yield chunk

    @timeout(10)
    def test_invalid_url(self):
        with self.assertRaises(requests.exceptions.InvalidURL):
            requests.get('http://.example.com')

    @timeout(10)
    def test_not_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=b'hello world', timeout=5.0)

    @timeout(10)
    def test_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=SendTest.data_chunked(), timeout=5.0)

    @timeout(10)
    def test_tuple_timeout_not_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=b'hello world', timeout=(5.0, 5.0))

    @timeout(10)
    def test_tuple_timeout_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=SendTest.data_chunked(), timeout=(5.0, 5.0))

    @timeout(10)
    def test_urllib3_timeout_not_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=b'hello world',
                     timeout=TimeoutSauce(5.0, 5.0))

    @timeout(10)
    def test_urllib3_timeout_chunked_data(self):
        requests.put('https://jsonplaceholder.typicode.com/posts/1', data=SendTest.data_chunked(),
                     timeout=TimeoutSauce(5.0, 5.0))

    @timeout(10)
    def test_invalid_timeout_not_chunked_data(self):
        with self.assertRaises(ValueError):
            requests.put('https://jsonplaceholder.typicode.com/posts/1', data=b'hello world', timeout=(5.0, 5.0, 5.0))

    @timeout(10)
    def test_invalid_timeout_chunked_data(self):
        with self.assertRaises(ValueError):
            requests.put('https://jsonplaceholder.typicode.com/posts/1', data=SendTest.data_chunked(),
                         timeout=(5.0, 5.0, 5.0))

    # @timeout(10)
    # def test_https_request_with_http_proxy_not_chunked_data(self):
    #     requests.put("https://www.google.com/", proxies={"http": 'http://localhost:3128'},
    #                  data=b'hello world')
    #
    # @timeout(10)
    # def test_https_request_with_https_proxy_not_chunked_data(self):
    #     requests.put("https://www.google.com/", proxies={"https": 'https://localhost:2137'},
    #                  data=b'hello world')
    #
    # @timeout(10)
    # def test_https_request_with_http_proxy_chunked_data(self):
    #     requests.put("https://www.google.com/", proxies={"http": 'http://localhost:3128'},
    #                  data=SendTest.data_chunked())
    #
    # @timeout(10)
    # def test_https_request_with_https_proxy_chunked_data(self):
    #     requests.put("https://www.google.com/", proxies={"https": 'https://localhost:2137'},
    #                  data=SendTest.data_chunked())

    @timeout(10)
    def test_connection_error(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get("http://0.0.0.0")

    @timeout(10)
    def test_timeout_not_chunked_data_non_responding_server(self):
        created_server_url = self.create_non_responding_server()
        with self.assertRaises(requests.exceptions.ReadTimeout):
            requests.put(created_server_url, data=b'hello world', timeout=5.0)

    # It's a bug, request's timeout is not working properly with chunked data and non responding server
    @timeout(10)
    def test_timeout_chunked_data_non_responding_server(self):
        created_server_url = self.create_non_responding_server()
        with self.assertRaises(requests.exceptions.ReadTimeout):
            requests.put(created_server_url, data=SendTest.data_chunked(), timeout=5.0)



