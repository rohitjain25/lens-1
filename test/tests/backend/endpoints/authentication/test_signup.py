import json
import requests
from tests.backend.constants import Schema_Files, Status_Code, Test_USER_Credentials

url = "http://localhost:8000/endpoints/auth/signup"


def test_auth_signup(framework):
    """Test to check the signup endpoint"""

    framework.log.info("Deleting user if already created")
    framework.delete_test_user()
    payload = {
        "email": Test_USER_Credentials.EMAIL,
        "password": Test_USER_Credentials.PASSWORD,
        "first_name": "String",
        "last_name": "String",
    }
    framework.log.step("Make a POST request to /endpoints/auth/signup")
    response = requests.post(url, json.dumps(payload))
    actual_response = response.json()

    framework.log.step("Verify 200 status code is returned")
    assert 201 == response.status_code, framework.log.error(
        f"Expected status code is {200} but got {response.status_code}"
    )

    framework.log.step("Verify response body")
    excepted_response = {
        "email": Test_USER_Credentials.EMAIL,
        "first_name": "String",
        "last_name": "String",
        "role": "level_5",
    }
    assert excepted_response == actual_response, framework.log.error(f'response is not as expected')
    framework.delete_test_user()


def test_auth_signup_twice(framework):
    """Test to check the signup endpoint"""

    framework.log.info("Deleting user if already created")
    framework.delete_test_user()
    payload = {
        "email": Test_USER_Credentials.EMAIL,
        "password": Test_USER_Credentials.PASSWORD,
        "first_name": "String",
        "last_name": "String",
    }
    
    framework.log.step("Make a POST request to /endpoints/auth/signup")
    response = requests.post(url, json.dumps(payload))
    actual_response = response.json()
    assert Status_Code.CREATED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.CREATED} but got {response.status_code}"
    )

    excepted_response = {
        "email": Test_USER_Credentials.EMAIL,
        "first_name": "String",
        "last_name": "String",
        "role": "level_5",
    }
    assert excepted_response == actual_response
    
    framework.log.step("Make a second POST request to /endpoints/auth/signup")
    response = requests.post(url, json.dumps(payload))
    actual_response = response.json()
    assert Status_Code.CONFLICT == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.CONFLICT} but got {response.status_code}"
    )
    
    assert framework.utility.response_validator(
        response.json(), Schema_Files.AUTHENTICATION
    )

    framework.delete_test_user()


def test_auth_signup_verbs(framework):
    """Tests that only POST method is allowed for /auth/signup and will return 405 for other methods."""

    framework.log.step("Call /endpoints/auth/signup with verb GET")
    headers = framework.get_admin_headers
    response = framework.requests.get(url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/signup with verb PATCH")
    response = framework.requests.patch(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/signup with verb PUT")
    response = framework.requests.put(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/signup with verb DELETE")
    response = framework.requests.delete(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/signup with verb OPTIONS")
    response = framework.requests.request(method="options", url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )


def test_auth_signup_invalid_password(framework):
    """Test the sign up endpoint returns a 401 if invalid credentials are provided."""

    framework.log.step("Call /endpoints/auth/signup with invalid credentials")
    payload = {
        "email": "test123@lens.com",
        "password": int(12345678),
        "last_name": "String",
        "first_name": "Dadaa"
    }
    response = framework.requests.post(url=url, payload=payload)
    assert Status_Code.BAD_REQUEST == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNPROCESSABLE_ENTITY} but actual is {response.status_code}"
    )

    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )
    
def test_auth_signup_invalid_first_name(framework):
    """Test the sign up endpoint returns a 401 if invalid credentials are provided."""

    framework.log.step("Call /endpoints/auth/signup with invalid first_name")
    payload = {
        "email": "test123@lens.com",
        "password": "test",
        "last_name": "String",
        "first_name": int(12345678)
    }
    response = framework.requests.post(url=url, payload=payload)
    assert Status_Code.BAD_REQUEST == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNPROCESSABLE_ENTITY} but actual is {response.status_code}"
    )

    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )

def test_auth_signup_invalid_last_name(framework):
    """Test the sign up endpoint returns a 401 if invalid credentials are provided."""

    framework.log.step("Call /endpoints/auth/signup with invalid first_name")
    payload = {
        "email": "test123@lens.com",
        "password": "test",
        "first_name": "String",
        "last_name": int(12345678)
    }
    response = framework.requests.post(url=url, payload=payload)
    assert Status_Code.BAD_REQUEST == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNPROCESSABLE_ENTITY} but actual is {response.status_code}"
    )

    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )
    
def test_auth_signup_invalid_email(framework):
    """Test the sign up endpoint returns a 401 if invalid credentials are provided."""

    framework.log.step("Call /endpoints/auth/signup with invalid first_name")
    payload = {
        "email": int(12345678),
        "password": "test",
        "first_name": "String",
        "last_name": "String"
    }
    response = framework.requests.post(url=url, payload=payload)
    assert Status_Code.BAD_REQUEST == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.UNPROCESSABLE_ENTITY} but actual is {response.status_code}"
    )

    assert framework.utility.response_validator(
        response.body, Schema_Files.AUTHENTICATION
    )
