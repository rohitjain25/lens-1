import json
import requests


def test_auth_signup(delete_user):
    """Test to check the signup endpoint"""

    url = "http://localhost:8000/endpoints/auth/signup"
    payload = {
        "email": "test_string1@gmail.com",
        "password": "string@123",
        "first_name": "String",
        "last_name": "String",
    }
    response = requests.post(url, json.dumps(payload))
    actual_response = response.json()
    assert 201 == response.status_code, print(f'Expected status code is {200} but got {response.status_code}')

    excepted_response = {
        "email": "test_string1@gmail.com",
        "first_name": "String",
        'last_name': 'String',
        "role": "level_5",
    }
    assert excepted_response == actual_response


def test_auth_delete(framework):
    """Test home page."""

    url = "http://localhost:8000/endpoints/auth/delete"
    payload = {"email": "test_string1@gmail.com"}
    headers = framework.get_admin_headers
    print(headers)
    response = framework.requests.post(url, payload, headers=headers)
    actual_response = response.body
    assert 201 == response.status_code, print(
        f"Expected status code is {201} but got {response.status_code}"
    )

    assert None == actual_response


def test_home2(requests):
    """Test home page."""

    url = "http://127.0.0.1:8000/"

    response = requests.get(url)
    actual_response = response.body
    assert 200 == response.status_code, print(
        f"Expected status code is {200} but got {response.status_code}"
    )

    excepted_response = {"Hello": "World"}

    assert excepted_response == actual_response


def test_home3(requests):
    """Test home page."""

    url = "http://127.0.0.1:8000/"

    response = requests.get(url)
    actual_response = response.body
    assert 200 == response.status_code, print(
        f"Expected status code is {200} but got {response.status_code}"
    )

    excepted_response = {"Hello": "World"}

    assert excepted_response == actual_response
