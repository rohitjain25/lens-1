import json
import requests
from tests.backend.constants import Schema_Files, Status_Code, Test_USER_Credentials

url = "http://localhost:8000/endpoints/auth/login"



def test_auth_login(framework):
    """Test to check the login endpoint"""

    framework.log.info("Adding Test User")
    framework.add_test_user('level_5')
    payload = {
        "email": Test_USER_Credentials.EMAIL,
        "password": Test_USER_Credentials.PASSWORD
    }
    framework.log.step("Make a POST request to /endpoints/auth/login")
    response = requests.post(url, json.dumps(payload))
    actual_response = response.json()

    framework.log.step("Verify 200 status code is returned")
    assert 201 == response.status_code, framework.log.error(
        f"Expected status code is {200} but got {response.status_code}"
    )

    framework.log.step("Verify response body")
    
    assert "token" in actual_response, framework.log.error(f'response is not as expected: {actual_response}')


def test_auth_login_verbs(framework):
    """Tests that only POST method is allowed for /auth/login and will return 405 for other methods."""

    framework.log.step("Call /endpoints/auth/login with verb GET")
    headers = framework.get_admin_headers
    response = framework.requests.get(url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb PATCH")
    response = framework.requests.patch(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb PUT")
    response = framework.requests.put(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb DELETE")
    response = framework.requests.delete(url=url, payload={}, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )

    framework.log.step("Call /endpoints/auth/login with verb OPTIONS")
    response = framework.requests.request(method="options", url=url, headers=headers)
    assert Status_Code.METHOD_NOT_ALLOWED == response.status_code, framework.log.error(
        f"Expected status code is {Status_Code.METHOD_NOT_ALLOWED} but actual is {response.status_Code}"
    )


def test_auth_login_invalid_email(framework):
    pass