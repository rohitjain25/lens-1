import json
import requests

from tests.backend.constants import Status_Code


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
    assert 201 == response.status_code, print(
        f"Expected status code is {200} but got {response.status_code}"
    )

    excepted_response = {
        "email": "test_string1@gmail.com",
        "first_name": "String",
        "last_name": "String",
        "role": "level_5",
    }
    assert excepted_response == actual_response


def test_auth_signup_verbs(framework):
    """Tests that only POST method is allowed for /auth/signup and will return 405 for other methods."""

    url = "http://localhost:8000/endpoints/auth/signup"

    print("Call /endpoints/auth/signup with verb GET")
    headers = framework.get_admin_headers
    response = framework.requests.get(url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED.value == response.status_code, print(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED.value} but actual is {response.status_Code}"
    )

    print("Call /endpoints/auth/signup with verb PATCH")
    response = framework.requests.patch(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED.value == response.status_code, print(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED.value} but actual is {response.status_Code}"
    )

    print("Call /endpoints/auth/signup with verb PUT")
    response = framework.requests.put(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED.value == response.status_code, print(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED.value} but actual is {response.status_Code}"
    )

    print("Call /endpoints/auth/signup with verb DELETE")
    response = framework.requests.delete(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED.value == response.status_code, print(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED.value} but actual is {response.status_Code}"
    )

    print("Call /endpoints/auth/signup with verb OPTIONS")
    response = framework.requests.request(method="options", url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED.value == response.status_code, print(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED.value} but actual is {response.status_Code}"
    )
