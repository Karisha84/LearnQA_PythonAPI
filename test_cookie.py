import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies
        print(cookie)
        cookie_value = response.cookies.get("HomeWork")
        print(cookie_value)

        assert "HomeWork" in response.cookies, "There is no cookie in the response"
        assert cookie_value == "hw_value", "Wrong cookie value"
