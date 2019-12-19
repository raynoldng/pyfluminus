import unittest
from unittest.mock import patch

from pyfluminus.tests.mock_server import MOCK_CONSTANTS
from pyfluminus.structs import Weblecture, Module
from pyfluminus import api

id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSIsImtpZCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSJ9.eyJpc3MiOiJodHRwczovL2x1bWludXMubnVzLmVkdS5zZy92Mi9hdXRoIiwiYXVkIjoidmVyc28iLCJleHAiOjE1NTIwMzQ4ODQsIm5iZiI6MTU1MjAzNDU4NCwibm9uY2UiOiJlYjA0Y2ZmN2U4YTg0YTM0YTlhOWE0YWI3NGU3NzE2NiIsImlhdCI6MTU1MjAzNDU4NCwiYXRfaGFzaCI6Im9RYmFrbkxxeUVPYWtWQV8tMjA2Q1EiLCJjX2hhc2giOiJfMi02T29UYjJJOUpFU2lDZEI2ZGVBIiwic2lkIjoiNTYyZGYxYWYyODRhMDA4MTY1MGE0MDQ4N2NhODAzOTgiLCJzdWIiOiIwMzA4OTI1Mi0wYzk2LTRmYWItYjA4MC1mMmFlYjA3ZWViMGYiLCJhdXRoX3RpbWUiOjE1NTIwMzQ1ODQsImlkcCI6Imlkc3J2IiwiYWRkcmVzcyI6IlJlcXVlc3QgYWxsIGNsYWltcyIsImFtciI6WyJwYXNzd29yZCJdfQ.R54fwml4-KmwaD_pNSJxmf3XXoQdf3coik7-c-Lt7dconpJHLlorsiymQaiGLTlUdvMGHYvN_1JzCi42azkCxF2kjAJiosdCigR3b4okM1sovXoJsbE7tIycx2jpZwCmusL6nMffzE0ly_Q28x55jdQmJ9PIyGe7XD4mfKqDweht4fhCAtoeJtNPeDKX2dG6p4ll0lJxgVBOZsdi8PYF6z_rTt7zmMgd9CSc6WH2sOl8f9FKpVxoGtLBmjEBcNbwODokTu-cgW20vLFc05a7UZa3uKzPZI3DONnUDptLGgatcYGmNDTooQrJdh5xDKrK1tmkgVgBTmvPb44WYIiqHw"
authorization = {"jwt": id_token}


class TestLesson(unittest.TestCase):
    def test_get_weblectures(self):
        test_module = Module(
                id='9db79e1f-4b15-4fe9-8783-363990eeff09',
                code='CS4261/CS5461',
                name='Algorithmic Mechanism Design',
                teaching=False,
                term='1910',
        )
        expected_weblectures = [
            Weblecture(
                id="12e82d43-46ae-4aff-a3b8-d65439787f67",
                name="CS4261/CS5461 Lecture on 8/16/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="a865596a-51b2-46c6-824b-91e017e6c81c",
                name="CS4261/CS5461 Lecture on 8/23/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="b16565e0-91a6-4378-8e14-0fc15ac94181",
                name="CS4261/CS5461 Lecture on 8/30/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="74c28182-04a7-4374-9741-6395e83f2ff4",
                name="CS4261/CS5461 Routing games on 9/6/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="3b553899-6fa2-4275-8231-f5bcaed94da6",
                name="CS4261/CS5461   Cooperative Games     on 9/13/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="177bb571-a61f-459a-8cee-af2eb46067b0",
                name="CS4261/CS5461   Algorithmic Mechanism Design     on 9/20/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="060cb69a-acd1-4daa-9f3e-75d1901423ae",
                name="CS4261/CS5461 Lecture on 10/4/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="3e9022c2-6293-43bb-8f42-23c08ce93609",
                name="CS4261/CS5461 Lecture on 10/11/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="7a462dfa-6bf4-4cf7-b2ef-b2b2776f65d4",
                name="CS4261/CS5461    Theorem (Lipton et al., 2004)     on 10/18/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="fb124655-7019-462b-b99c-2fd9fa64c74a",
                name="CS4261/CS5461 Lecture on 10/25/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="3a9b60dc-57d6-4e39-8030-0e6792739258",
                name="CS4261/CS5461   Mechanism Design      on 11/1/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="29ee0f3e-9eef-4494-bf4d-07c8cb36ef49",
                name="CS4261/CS5461 Lecture on 11/8/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Weblecture(
                id="23850eee-2e5b-422e-8d39-176ad2974093",
                name="CS4261/CS5461 Lecture on 11/15/2019 (Fri)",
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
        ]
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            weblectures = test_module.weblectures(authorization)

        self.assertEqual(len(weblectures), len(expected_weblectures))
        for w1, w2 in zip(weblectures, expected_weblectures):
            self.assertEqual(w1, w2)