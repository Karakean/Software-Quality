import requests
import time

class Test:
    def __init__(self, num_requests, concurrency, timeout):    
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.timeout = timeout

# funkcja wykonywana w wielu wątkach
def make_request(session, timeout, url):
    try:
        response = session.get(url, timeout=timeout)
        return response.status_code
    except requests.exceptions.RequestException:
        return None

# funkcja uruchamiająca test
def run_test(url, num_requests, concurrency, timeout):
    with requests.Session() as session:
        session.headers.update({'Connection': 'keep-alive'})
        session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=concurrency, pool_maxsize=concurrency))
        start_time = time.time()
        responses = [make_request(session, timeout, url) for _ in range(num_requests)]
        elapsed_time = time.time() - start_time
    return elapsed_time, responses

tests = [
    Test(1, 1, 5),
    Test(10, 1, 5),
    Test(100, 1, 5),
    Test(10, 10, 5),
    Test(100, 10, 5),
    Test(1000, 10, 5),
]

for test in tests:
    # uruchomienie testu
    elapsed_time, responses = run_test("http://example.com", test.num_requests, test.concurrency, test.timeout)

    # wyniki testu
    print(f"Czas wykonania {test.num_requests} żądań: {elapsed_time:.3f} s")
    print(f"Średni czas na żądanie: {elapsed_time/test.num_requests:.3f} s")
    print(f"Liczba błędnych żądań: {responses.count(None)}")
    print(f"Kod statusu najwolniejszego zakończonego żądania: {max(response for response in responses if response is not None)}")


