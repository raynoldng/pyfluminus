# Third-party imports...
from unittest.mock import patch
from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

# Local imports...
# from project.services import get_users
from pyfluminus.tests.mock_server import get_free_port, start_mock_server, MOCK_CONSTANTS

from pyfluminus import api

id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSIsImtpZCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSJ9.eyJpc3MiOiJodHRwczovL2x1bWludXMubnVzLmVkdS5zZy92Mi9hdXRoIiwiYXVkIjoidmVyc28iLCJleHAiOjE1NTIwMzQ4ODQsIm5iZiI6MTU1MjAzNDU4NCwibm9uY2UiOiJlYjA0Y2ZmN2U4YTg0YTM0YTlhOWE0YWI3NGU3NzE2NiIsImlhdCI6MTU1MjAzNDU4NCwiYXRfaGFzaCI6Im9RYmFrbkxxeUVPYWtWQV8tMjA2Q1EiLCJjX2hhc2giOiJfMi02T29UYjJJOUpFU2lDZEI2ZGVBIiwic2lkIjoiNTYyZGYxYWYyODRhMDA4MTY1MGE0MDQ4N2NhODAzOTgiLCJzdWIiOiIwMzA4OTI1Mi0wYzk2LTRmYWItYjA4MC1mMmFlYjA3ZWViMGYiLCJhdXRoX3RpbWUiOjE1NTIwMzQ1ODQsImlkcCI6Imlkc3J2IiwiYWRkcmVzcyI6IlJlcXVlc3QgYWxsIGNsYWltcyIsImFtciI6WyJwYXNzd29yZCJdfQ.R54fwml4-KmwaD_pNSJxmf3XXoQdf3coik7-c-Lt7dconpJHLlorsiymQaiGLTlUdvMGHYvN_1JzCi42azkCxF2kjAJiosdCigR3b4okM1sovXoJsbE7tIycx2jpZwCmusL6nMffzE0ly_Q28x55jdQmJ9PIyGe7XD4mfKqDweht4fhCAtoeJtNPeDKX2dG6p4ll0lJxgVBOZsdi8PYF6z_rTt7zmMgd9CSc6WH2sOl8f9FKpVxoGtLBmjEBcNbwODokTu-cgW20vLFc05a7UZa3uKzPZI3DONnUDptLGgatcYGmNDTooQrJdh5xDKrK1tmkgVgBTmvPb44WYIiqHw"
authorization = {"jwt": id_token}

class TestMockServer(object):
    @classmethod
    def setup_class(cls):
        # cls.mock_server_port = get_free_port()
        # start_mock_server(cls.mock_server_port)
        start_mock_server(8082) # for API

    # def test_request_response(self):
    #     mock_users_url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)

    #     # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
    #     with patch.dict('pyfluminus.constants.__dict__', MOCK_CONSTANTS):
    #         response = get_users()

    #     assert_dict_contains_subset({'Content-Type': 'application/json; charset=utf-8'}, response.headers)
    #     assert_true(response.ok)
    #     assert_list_equal(response.json(), [])

    def test_get_profile(self):
        # TODO, copy dict and then extend with mock 
        with patch.dict('pyfluminus.api.__dict__', MOCK_CONSTANTS): 
            assert api.name(authorization) == 'John Smith'

