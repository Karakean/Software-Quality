import requests
import traceback
import sys
from inspect import isfunction


def test_get_request():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200
    assert response.json()['userId'] == 1
    assert response.json()['id'] == 1


def test_list_get_request():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    assert response.status_code == 200
    data = response.json()
    i = 1
    j = 1
    for element in data:
        assert element['userId'] == i
        assert element['id'] == j
        if j % 10 == 0:
            i += 1
        j += 1


def test_post_request():
    test_object = {'postTestKey': 'postTestValue'}
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=test_object)
    assert response.status_code == 201
    assert response.json()['id'] == 101
    assert response.json()['postTestKey'] == 'postTestValue'


def test_put_request():
    test_object = {'putTestKey': 'putTestValue'}
    response = requests.put('https://jsonplaceholder.typicode.com/posts/1', json=test_object)
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['putTestKey'] == 'putTestValue'


def test_delete_request():
    response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200
    assert str(response.json()) == "{}"


def test_head_request():
    response = requests.head('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200


def test_patch_request():
    test_object = {'patchTestKey': 'patchTestValue'}
    response = requests.patch('https://jsonplaceholder.typicode.com/posts/1', json=test_object)
    assert response.status_code == 200
    assert response.json()['userId'] == 1
    assert response.json()['id'] == 1
    assert response.json()['patchTestKey'] == 'patchTestValue'


def test_options_request():
    response = requests.options('https://www.example.com')
    assert response.status_code == 200
    assert response.headers['Allow'] == 'OPTIONS, GET, HEAD, POST'


def test_redirection_handling():
    url = "http://httpbin.org/redirect-to?url=https://www.example.com"
    response = requests.get(url)
    assert response.url == "https://www.example.com"


def test_authentication_with_correct_credentials():
    username = 'testUsername'
    password = 'testPassword'
    response = requests.get(f'http://httpbin.org/basic-auth/{username}/{password}', auth=(username, password))
    assert response.status_code == 200
    assert response.json()['authenticated']
    assert response.json()['user'] == f'{username}'


def test_authentication_with_wrong_credentials():
    username = 'correctUsername'
    password = 'correctPassword'
    response = requests.get(f'http://httpbin.org/basic-auth/{username}/{password}', auth=('wrongUsername', 'wrongPassword'))
    assert response.status_code == 401


# It's a bug, popitem() should raise KeyError only if cookies are empty, but it is raised even when they're not
def test_pop_cookie():
    r = requests.get('https://google.com')
    init_cookie_count = len(r.cookies)
    r.cookies.popitem()
    assert len(r.cookies) == init_cookie_count - 1


def run_all_tests():
    tests = [test_get_request, test_list_get_request, test_post_request, test_put_request, test_delete_request,
             test_head_request, test_patch_request, test_options_request, test_redirection_handling,
             test_authentication_with_correct_credentials, test_authentication_with_wrong_credentials, test_pop_cookie]
    failed_tests = 0
    for i, test in enumerate(tests):
        try:
            test()
        except Exception:
            print(f'Test {tests[i]} failed. Caused by:\n{traceback.format_exc()}')
            failed_tests += 1
    if failed_tests == 0:
        print(f'All {len(tests)} tests passed :)')
    else:
        print(f'There were failing tests. {len(tests) - failed_tests} tests passed, {failed_tests} failed.')


def run_particular_test(test):
    try:
        test()
        print(f'Test {test.__name__} passed. :)')
    except Exception:
        print(f'Test {test.__name__} failed. Caused by:\n{traceback.format_exc()}')


def main():
    if len(sys.argv) <= 1:
        run_all_tests()
        return
    for test in sys.argv[1:]:
        if test in globals() and callable(globals().get(test)):
            run_particular_test(globals().get(test))
        else:
            print(f'Invalid test name passed: {test}')


if __name__ == "__main__":
    main()
