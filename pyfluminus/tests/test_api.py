import unittest
from unittest.mock import patch

from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

from pyfluminus.tests.mock_server import MOCK_CONSTANTS
from pyfluminus.structs import Module, Lesson, File, Weblecture
from pyfluminus import api

id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSIsImtpZCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSJ9.eyJpc3MiOiJodHRwczovL2x1bWludXMubnVzLmVkdS5zZy92Mi9hdXRoIiwiYXVkIjoidmVyc28iLCJleHAiOjE1NTIwMzQ4ODQsIm5iZiI6MTU1MjAzNDU4NCwibm9uY2UiOiJlYjA0Y2ZmN2U4YTg0YTM0YTlhOWE0YWI3NGU3NzE2NiIsImlhdCI6MTU1MjAzNDU4NCwiYXRfaGFzaCI6Im9RYmFrbkxxeUVPYWtWQV8tMjA2Q1EiLCJjX2hhc2giOiJfMi02T29UYjJJOUpFU2lDZEI2ZGVBIiwic2lkIjoiNTYyZGYxYWYyODRhMDA4MTY1MGE0MDQ4N2NhODAzOTgiLCJzdWIiOiIwMzA4OTI1Mi0wYzk2LTRmYWItYjA4MC1mMmFlYjA3ZWViMGYiLCJhdXRoX3RpbWUiOjE1NTIwMzQ1ODQsImlkcCI6Imlkc3J2IiwiYWRkcmVzcyI6IlJlcXVlc3QgYWxsIGNsYWltcyIsImFtciI6WyJwYXNzd29yZCJdfQ.R54fwml4-KmwaD_pNSJxmf3XXoQdf3coik7-c-Lt7dconpJHLlorsiymQaiGLTlUdvMGHYvN_1JzCi42azkCxF2kjAJiosdCigR3b4okM1sovXoJsbE7tIycx2jpZwCmusL6nMffzE0ly_Q28x55jdQmJ9PIyGe7XD4mfKqDweht4fhCAtoeJtNPeDKX2dG6p4ll0lJxgVBOZsdi8PYF6z_rTt7zmMgd9CSc6WH2sOl8f9FKpVxoGtLBmjEBcNbwODokTu-cgW20vLFc05a7UZa3uKzPZI3DONnUDptLGgatcYGmNDTooQrJdh5xDKrK1tmkgVgBTmvPb44WYIiqHw"
authorization = {"jwt": id_token}


class TestAPI(unittest.TestCase):

    def test_get_profile(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.name(authorization)
            self.assertTrue(result.okay)
            self.assertEqual(result.data, "John Smith")

    def test_get_current_term(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.current_term(authorization)
        self.assertTrue(result.okay)
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

        self.assertTrue(result.okay)
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

    def test_get_lessons(self):
        expected_lessons = [
            Lesson(
                id="e344491c-dc7a-493b-88f3-db9157e2853b",
                name="Week 7: ",
                week=7,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="f538653c-af50-42d2-8b7b-898e8f941998",
                name="Week 8: ",
                week=8,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="fc27c2ab-b790-4f8e-b2ce-07b5757d8189",
                name="Week 9: ",
                week=9,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="9991c6cc-a05d-4962-ba6c-f9fa47aed573",
                name="Week 10: ",
                week=10,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="7760a4e3-57e2-435b-a6d9-494e8ac7ed30",
                name="Week 11: ",
                week=11,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="4d2de7e3-9ab4-4cf3-b29e-cc8a2d7f1382",
                name="Week 12: ",
                week=12,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
            Lesson(
                id="e75410c3-ee66-4631-8b7b-b2dd744e839a",
                name="Week 13: ",
                week=13,
                module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
            ),
        ]

        module_id = "9db79e1f-4b15-4fe9-8783-363990eeff09"
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.get_lessons(authorization, module_id)

        lessons = result.data

        self.assertEqual(len(lessons), len(expected_lessons))
        for lesson1, lesson2 in zip(lessons, expected_lessons):
            self.assertEqual(lesson1, lesson2)

    def test_get_lesson_files(self):
        lesson = Lesson(
            id="e344491c-dc7a-493b-88f3-db9157e2853b",
            name="Week 7: ",
            week=7,
            module_id="9db79e1f-4b15-4fe9-8783-363990eeff09",
        )
        expected_file = File(
            id="e2a3bfa1-78d2-400b-ac74-c09636131b6f",
            name="Lesson 6 - CS4261 - The Bargaining Solution.pdf",
            children=[],
            allow_upload=False,
            multimedia=False,
            directory=False,
        )

        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = api.get_files_from_lesson(authorization, lesson)
        self.assertTrue(result.okay)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0], expected_file)

    def test_get_weblectures(self):
        module_id = "9db79e1f-4b15-4fe9-8783-363990eeff09"
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
            result = api.get_weblectures(authorization, module_id)

        self.assertTrue(result.okay)
        weblectures = result.data
        self.assertEqual(len(weblectures), len(expected_weblectures))
        for w1, w2 in zip(weblectures, expected_weblectures):
            self.assertEqual(w1, w2)
