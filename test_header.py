import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.text)

        assert 'success":"!"' in response.text, "There is no text"
