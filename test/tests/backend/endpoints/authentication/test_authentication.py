import json
import requests


def test_auth_signup(framework):
    """Test to check the signup endpoint"""

    framework.delete_user
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
