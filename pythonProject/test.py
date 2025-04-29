import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        headers_value = response.headers.get("x-secret-homework-header")
        print(headers_value)

        assert 'x-secret-homework-header' in response.headers, "There is no header in response"
        assert headers_value == "Some secret value", "Wrong headers value"
