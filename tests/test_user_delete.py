import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_user__with_number_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )
        Assertions.assert_code_status(response2, 400)

    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}")
        Assertions.assert_code_status(response4, 404)

    def test_delete_user_with_other_user(self):
        # REGISTER 1
        register_data_first_user = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_first_user)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_first_user = register_data_first_user['email']
        password_first_user = register_data_first_user['password']

        # REGISTER 2
        register_data_second_user = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_second_user)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id_second_user = self.get_json_value(response2, 'id')

        # LOGIN first user
        login_data = {
            'email': email_first_user,
            'password': password_first_user
        }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid_first_user = self.get_cookie(response3, "auth_sid")
        token_first_user = self.get_header(response3, "x-csrf-token")

        # DELETE second user with first user login
        response4 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_second_user}",
                                    headers={"x-csrf-token": token_first_user},
                                    cookies={"auth_sid": auth_sid_first_user}
                                    )
        # GET
        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_second_user}")
        Assertions.assert_code_status(response5, 200)
