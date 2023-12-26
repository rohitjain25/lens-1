import pytest


@pytest.fixture
def delete_user(requests):
    url = "http://127.0.0.1:8000/endpoints/auth/login/"
    payload = {"email": "admin@lens.com", "password": "admin"}
    response = requests.post(url, payload)
    token = response.body["token"]
    headers = {"Authorization": f"Bearer {token}"}
    url_2 = "http://localhost:8000/endpoints/auth/delete"
    payload_2 = {"email": "test_string1@gmail.com"}
    response = requests.post(url_2, payload_2, headers=headers)
    assert 201 == response.status_code, print(f'Expected status code is {201} but got {response.status_code}')
    
@pytest.fixture
def framework(requests):
    return _Framework(requests)


class _Framework:
    def __init__(self, requests):
        self.requests = requests
    
    @property    
    def get_admin_headers(self):
        url = "http://127.0.0.1:8000/endpoints/auth/login/"
        payload = {"email": "admin@lens.com", "password": "admin"}
        response = self.requests.post(url, payload)
        assert 200 == response.status_code, print(f'Expected status code is {200} but got {response.status_code}')
        token = response.body["token"]
        headers = {"Authorization": f"Bearer {token}"}
        return headers