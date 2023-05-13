import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEditNegative(BaseCase):
    def test_user_edit_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = 'Changed Name'

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 400)

    def test_user_edit_with_other_auth(self):
        # REGISTER 1
        register_data_first_user = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_first_user)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_first_user = register_data_first_user['email']
        password_first_user = register_data_first_user['password']
        name_first_user = register_data_first_user['firstName']
        user_id_first_user = self.get_json_value(response1, 'id')

        # REGISTER 2
        register_data_second_user = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_second_user)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email_second_user = register_data_second_user['email']
        password_second_user = register_data_second_user['password']

        # LOGIN first user
        login_data = {
            'email': email_first_user,
            'password': password_first_user
        }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid_first_user = self.get_cookie(response3, "auth_sid")
        token_first_user = self.get_header(response3, "x-csrf-token")

        # LOGIN second
        login_data = {
            'email': email_second_user,
            'password': password_second_user
        }
        response4 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid_second_user = self.get_cookie(response4, "auth_sid")
        token_second_user = self.get_header(response4, "x-csrf-token")

        # EDIT FIRST USER WITH AUTH SECOND USER
        new_name = 'Changed Name'

        requests.put(f"https://playground.learnqa.ru/api/user/{user_id_first_user}",
                                 headers={"x-csrf-token": token_second_user},
                                 cookies={"auth_sid":  auth_sid_second_user},
                                 data={"firstName": new_name}
                                 )

        # GET
        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_first_user}",
                                 headers={"x-csrf-token": token_first_user},
                                 cookies={"auth_sid": auth_sid_first_user}
                                 )
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            name_first_user,
            "Name is changed"
        )



    def test_user_edit_with_wrong_email(self):
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

        # EDIT
        new_email = 'usermail.ru'

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email}
                                 )

        Assertions.assert_code_status(response3, 400)

    def test_user_edit_with_short_first_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
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

        # EDIT
        new_first_name = 'a'

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName":  new_first_name}
                                 )

