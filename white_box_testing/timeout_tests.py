import socket
import threading
import requests
import pytest


def mock_server():
    mocked_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mocked_server.bind(('localhost', 0))
    mocked_server.listen()
    mocked_server_port = mocked_server.getsockname()[1]
    server_thread = threading.Thread(target=handle_requests, args=(mocked_server,))
    server_thread.start()
    return f'http://localhost:{mocked_server_port}'


def handle_requests(mocked_server):
    while True:
        client_socket, _ = mocked_server.accept()
        request_data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            request_data += chunk


def data_chunked():
    data = [b'hello', b'world']
    for chunk in data:
        yield chunk


def test_timeout_1():
    mock_server_url = mock_server()
    requests.put(mock_server_url, data=b'hello', timeout=5.0)
    requests.put(f'{mock_server_url}/shutdown')


def test_timeout_2():
    mock_server_url = mock_server()
    requests.put(mock_server_url, data=data_chunked(), timeout=5.0)
    requests.put(f'{mock_server_url}/shutdown')


def main():
    test_timeout_1()
    test_timeout_2()


main()
