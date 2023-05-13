import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    data = ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotovexample.com'},
            {'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotovexample.com'},
            {'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotovexample.com'},
            {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'vinkotovexample.com'},
            {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}
            )

    def test_create_user_sucessfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('data', data)
    def test_cannot_create_user_without_required_field(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)

    def test_create_user_with_short_username(self):
        username = 'a'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov1@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_username(self):
        username = 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' \
                   'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' \
                   'sssssssssssssssssssssssssssssssssssssssssssssssssssssds'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov2@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"
