import unittest
from unittest.mock import patch

from nose.tools import (assert_dict_contains_subset, assert_list_equal,
                        assert_true)

from pyfluminus import api
from pyfluminus.structs import Lesson, Module
from pyfluminus.tests.mock_server import MOCK_CONSTANTS

id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSIsImtpZCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSJ9.eyJpc3MiOiJodHRwczovL2x1bWludXMubnVzLmVkdS5zZy92Mi9hdXRoIiwiYXVkIjoidmVyc28iLCJleHAiOjE1NTIwMzQ4ODQsIm5iZiI6MTU1MjAzNDU4NCwibm9uY2UiOiJlYjA0Y2ZmN2U4YTg0YTM0YTlhOWE0YWI3NGU3NzE2NiIsImlhdCI6MTU1MjAzNDU4NCwiYXRfaGFzaCI6Im9RYmFrbkxxeUVPYWtWQV8tMjA2Q1EiLCJjX2hhc2giOiJfMi02T29UYjJJOUpFU2lDZEI2ZGVBIiwic2lkIjoiNTYyZGYxYWYyODRhMDA4MTY1MGE0MDQ4N2NhODAzOTgiLCJzdWIiOiIwMzA4OTI1Mi0wYzk2LTRmYWItYjA4MC1mMmFlYjA3ZWViMGYiLCJhdXRoX3RpbWUiOjE1NTIwMzQ1ODQsImlkcCI6Imlkc3J2IiwiYWRkcmVzcyI6IlJlcXVlc3QgYWxsIGNsYWltcyIsImFtciI6WyJwYXNzd29yZCJdfQ.R54fwml4-KmwaD_pNSJxmf3XXoQdf3coik7-c-Lt7dconpJHLlorsiymQaiGLTlUdvMGHYvN_1JzCi42azkCxF2kjAJiosdCigR3b4okM1sovXoJsbE7tIycx2jpZwCmusL6nMffzE0ly_Q28x55jdQmJ9PIyGe7XD4mfKqDweht4fhCAtoeJtNPeDKX2dG6p4ll0lJxgVBOZsdi8PYF6z_rTt7zmMgd9CSc6WH2sOl8f9FKpVxoGtLBmjEBcNbwODokTu-cgW20vLFc05a7UZa3uKzPZI3DONnUDptLGgatcYGmNDTooQrJdh5xDKrK1tmkgVgBTmvPb44WYIiqHw"
authorization = {"jwt": id_token}


class TestAPI(unittest.TestCase):

    def test_get_profile(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.name(authorization)
            self.assertTrue(result.ok)
            self.assertEqual(result.data, "John Smith")

    def test_get_current_term(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.current_term(authorization)
        self.assertTrue(result.ok)
        self.assertDictEqual(
            result.data, {"term": "1820", "description": "2018/2019 Semester 2"}
        )

    def test_get_modules(self):
        expected_modules = [
            Module(
                code="CS1101S",
                id="57290e55-335a-4c09-b904-a795572d6cda",
                name="Programming Methodology",
                teaching=True,
                term="1910",
            ),
            Module(
                code="CS2106",
                id="41cc9aa5-6704-48c1-a61c-4fe75ed085f6",
                name="Introduction to Operating Systems",
                teaching=False,
                term="1810",
            ),
            Module(
                code="CS2100",
                id="063773a9-43ac-4dc0-bdc6-4be2f5b50300",
                name="Computer Organisation",
                teaching=True,
                term="1820",
            ),
            Module(
                code="ST2334",
                id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",
                name="Probability and Statistics",
                teaching=False,
                term="1820",
            ),
            Module(
                code="CS1101S",
                id="8722e9a5-abc5-4160-820d-bf69d8a63c6f",
                name="Programming Methodology",
                teaching=True,
                term="1810",
            ),
        ]
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.modules(authorization)

        self.assertTrue(result.ok)
        modules = result.data
        modules.sort(key=lambda mod: mod.id)
        expected_modules.sort(key=lambda mod: mod.id)

        self.assertEqual(len(modules), len(expected_modules))
        for mod1, mod2 in zip(modules, expected_modules):
            self.assertEqual(mod1, mod2)

    def get_current_term_modules(self):
        expected_modules = [
            Module(
                code="CS2100",
                id="063773a9-43ac-4dc0-bdc6-4be2f5b50300",
                name="Computer Organisation",
                teaching=True,
                term="1820",
            ),
            Module(
                code="ST2334",
                id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",
                name="Probability and Statistics",
                teaching=False,
                term="1820",
            ),
        ]
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.modules(authorization, current_term_only=True)

        modules = result.data
        modules.sort(key=lambda mod: mod.id)
        expected_modules.sort(key=lambda mod: mod.id)

        self.assertEqual(len(modules), len(expected_modules))
        for mod1, mod2 in zip(modules, expected_modules):
            self.assertEqual(mod1, mod2)
