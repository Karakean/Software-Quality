import requests
import time

class Result:
    def __init__(self, time, file_size, status):
        self.time = time
        self.file_size = file_size
        self.status = status

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

def test_speed(filename):
    start_time = time.time()
    response = requests.get(url + filename)
    end_time = time.time()

    file_size = len(response.content) / (1024*1024) # Convert bytes to MB
    download_time = end_time - start_time
    return Result(download_time, file_size, response.status_code)

url = 'http://speedtest.tele2.net/'

files = [
    File("1MB.zip", 1),
    File("10MB.zip", 10),
    File("100MB.zip", 100)
]

for file in files:
    result = test_speed(file.name)
    print(f"Czas pobierania pliku: {result.time:.3f} s")
    print(f"Rozmiar pliku: {result.file_size} MB")
    print(f"Status odpowiedzi: {result.status}")

# print(f"Downloaded {file_size:.2f} MB in {download_time:.2f} seconds.")