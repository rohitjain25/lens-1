import pytest

from setup.utility import Utility
from tests.backend.constants import Status_Code, Test_USER_Credentials


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope='function')
def framework(request, requests, log):
    print()
    log.info(f'Starting test execution for {request.node.name}')
    fixtures = {"request": request, "requests": requests, "log": log}
    yield _Framework(fixtures)
    setup_passed = request.node.rep_setup.passed if request.node.rep_setup else True
    call_passed = request.node.rep_call.passed if request.node.rep_call else False
    if setup_passed and call_passed:
        print("\033[32mPassed\x1b[0m")
    else:print("Failed")
        

class _Framework:
    __utility = None

    def __init__(self, fixtures):
        self.__request = fixtures["request"]
        self.requests = fixtures["requests"]
        self.log = fixtures["log"]
        self.__add_admin_user()
        self.__request.addfinalizer(self._test_passed)
        self.__request.addfinalizer(self.__delete_admin_user)

    def _test_passed(self):
        return
        setup_passed = self.__request.node.rep_setup.passed if self.__request.node.rep_setup else True
        call_passed = self.__request.node.rep_call.passed if self.__request.node.rep_call else False
        if setup_passed and call_passed:
            print("\x1b[31;20mPassed\x1b[0m")
            

    @property
    def get_admin_headers(self):
        url = "http://127.0.0.1:8000/endpoints/auth/login/"
        payload = {"email": "testadmin@lens.com", "password": "admin"}
        response = self.requests.post(url, payload)
        self.log.info("Verify 201 status code is returned")
        assert 201 == response.status_code, self.log.error(
            f"Expected status code is {201} but got {response.status_code}"
        )
        token = response.body["token"]
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    def delete_test_user(self):
        self.log.info("Deleting Test User")
        headers = self.get_admin_headers
        url_2 = "http://localhost:8000/endpoints/auth/delete"
        payload_2 = {"email": Test_USER_Credentials.EMAIL}
        response = self.requests.post(url_2, payload_2, headers=headers)
        self.log.info("Verify 201 status code is returned")
        assert 201 == response.status_code, self.log.error(
            f"Expected status code is {201} but got {response.status_code}"
        )

    def __add_admin_user(self):
        self.log.info("Creating Admin User")
        payload = {
            "email": "testadmin@lens.com",
            "password": "admin",
            "first_name": "admin",
            "last_name": "admin",
            "role": "level_1",
        }
        url = "http://127.0.0.1:8000/endpoints/auth/signup/"
        response = self.requests.post(url, payload)
        self.log.info("Verify 201 status code is returned")
        assert Status_Code.CREATED == response.status_code, self.log.error(
            f"expected status code is {Status_Code.CREATED} but actual is {response.status_code}"
        )

    def __delete_admin_user(self):
        self.log.info("Deleting Admin User")
        headers = self.get_admin_headers
        url_2 = "http://localhost:8000/endpoints/auth/delete"
        payload_2 = {"email": "testadmin@lens.com"}
        response = self.requests.post(url_2, payload_2, headers=headers)
        self.log.info("Verify 201 status code is returned")
        assert 201 == response.status_code, self.log.error(
            f"Expected status code is {201} but got {response.status_code}"
        )

    def add_test_user(self, role: str='level_5'):
        self.__request.addfinalizer(self.delete_test_user)
        payload = {
            "email": Test_USER_Credentials.EMAIL,
            "password": Test_USER_Credentials.PASSWORD,
            "first_name": "test",
            "last_name": "test",
            "role": role,
        }
        url = "http://127.0.0.1:8000/endpoints/auth/signup/"
        response = self.requests.post(url, payload)
        self.log.info("Verify 201 status code is returned")
        assert Status_Code.CREATED == response.status_code, self.log.error(
            f"Expected status code is {201} but got {response.status_code}"
        )

    @property
    def utility(self):
        if self.__utility is None:
            self.__utility = Utility()
        return self.__utility
