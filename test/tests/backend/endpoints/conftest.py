import pytest

from setup.utility import Utility


@pytest.fixture
def framework(requests):
    return _Framework(requests)


class _Framework:
    __utility = None
    
    def __init__(self, requests):
        self.requests = requests

    @property
    def get_admin_headers(self):
        url = "http://127.0.0.1:8000/endpoints/auth/login/"
        payload = {"email": "admin@lens.com", "password": "admin"}
        response = self.requests.post(url, payload)
        assert 201 == response.status_code, print(
            f"Expected status code is {201} but got {response.status_code}"
        )
        token = response.body["token"]
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    @property
    def delete_user(self):
        self.__add_admin_user()
        headers = self.get_admin_headers
        url_2 = "http://localhost:8000/endpoints/auth/delete"
        payload_2 = {"email": "test_string1@gmail.com"}
        response = self.requests.post(url_2, payload_2, headers=headers)
        assert 201 == response.status_code, print(
            f"Expected status code is {201} but got {response.status_code}"
        )

    def __add_admin_user(self):
        payload = {
            "email": "admin@lens.com",
            "password": "admin",
            "first_name": "admin",
            "last_name": "admin",
            "role": "level_1"
        }
        url = "http://127.0.0.1:8000/endpoints/auth/signup/"
        response = self.requests.post(url, payload)
        print("adding admin user", "success" if response.status_code == 201 else "failed")

    @property
    def utility(self):
        if self.__utility is None:
            self.__utility = Utility()
        return self.__utility