import requests
import json

class Requests:
    def __init__(self):
        pass
        
    def get(self, url, headers=None):
        response = requests.get(url=url, headers=headers)
        return _Response(response)

    def post(self, url, payload, headers=None):
        payload = json.dumps(payload)
        response = requests.post(url=url, data=payload, headers=headers)
        return _Response(response)

    def patch(self, url, payload, headers=None):
        payload = json.dumps(payload)
        response = requests.patch(url=url, data=payload, headers=headers)
        return _Response(response)

    def put(self, url, payload, headers=None):
        payload = json.dumps(payload)
        response = requests.put(url=url, data=payload, headers=headers)
        return _Response(response)

    def delete(self, url, payload, headers=None):
        payload = json.dumps(payload)
        response = requests.delete(url=url, data=payload, headers=headers)
        return _Response(response)

    def request(self, method, url, payload=None, headers=None):
        if payload:
            payload = json.dumps(payload)
        response = requests.request(method=method, url=url, data=payload, headers=headers)
        return _Response(response)

class _Response:
    """A class to wrap the actual request's Response object with a more user-friendly interface."""
    def __init__(self, response:requests.Response):
        self.status_code = response.status_code
        self.body = response.json()
        self.headers = response.headers
        self.cookies = response.cookies