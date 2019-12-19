import unittest
from unittest.mock import patch
import os, shutil
from dateutil.parser import parse

from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

from pyfluminus.tests.mock_server import MOCK_CONSTANTS
from pyfluminus.structs import Module, File, Lesson
from pyfluminus import api
from pyfluminus.constants import ErrorTypes

temp_dir = "test/temp/api/file/"
id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSIsImtpZCI6ImEzck1VZ01Gdjl0UGNsTGE2eUYzekFrZnF1RSJ9.eyJpc3MiOiJodHRwczovL2x1bWludXMubnVzLmVkdS5zZy92Mi9hdXRoIiwiYXVkIjoidmVyc28iLCJleHAiOjE1NTIwMzQ4ODQsIm5iZiI6MTU1MjAzNDU4NCwibm9uY2UiOiJlYjA0Y2ZmN2U4YTg0YTM0YTlhOWE0YWI3NGU3NzE2NiIsImlhdCI6MTU1MjAzNDU4NCwiYXRfaGFzaCI6Im9RYmFrbkxxeUVPYWtWQV8tMjA2Q1EiLCJjX2hhc2giOiJfMi02T29UYjJJOUpFU2lDZEI2ZGVBIiwic2lkIjoiNTYyZGYxYWYyODRhMDA4MTY1MGE0MDQ4N2NhODAzOTgiLCJzdWIiOiIwMzA4OTI1Mi0wYzk2LTRmYWItYjA4MC1mMmFlYjA3ZWViMGYiLCJhdXRoX3RpbWUiOjE1NTIwMzQ1ODQsImlkcCI6Imlkc3J2IiwiYWRkcmVzcyI6IlJlcXVlc3QgYWxsIGNsYWltcyIsImFtciI6WyJwYXNzd29yZCJdfQ.R54fwml4-KmwaD_pNSJxmf3XXoQdf3coik7-c-Lt7dconpJHLlorsiymQaiGLTlUdvMGHYvN_1JzCi42azkCxF2kjAJiosdCigR3b4okM1sovXoJsbE7tIycx2jpZwCmusL6nMffzE0ly_Q28x55jdQmJ9PIyGe7XD4mfKqDweht4fhCAtoeJtNPeDKX2dG6p4ll0lJxgVBOZsdi8PYF6z_rTt7zmMgd9CSc6WH2sOl8f9FKpVxoGtLBmjEBcNbwODokTu-cgW20vLFc05a7UZa3uKzPZI3DONnUDptLGgatcYGmNDTooQrJdh5xDKrK1tmkgVgBTmvPb44WYIiqHw"
authorization = {"jwt": id_token}

module = Module(
    code="ST2334",
    id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",
    name="Probability and Statistics",
    teaching=False,
    term="1820",
)


class TestModule(unittest.TestCase):
    def test_from_api(self):
        api_data = {
            "id": "57290e55-335a-4c09-b904-a795572d6cda",
            "name": "CS1101S",
            "courseName": "Programming Methodology",
            "access": {
                "access_Full": True,
                "access_Create": True,
                "access_Update": True,
                "access_Delete": True,
                "access_Settings_Read": True,
                "access_Settings_Update": True,
            },
            "term": "1820",
        }
        expected_module = Module(
            id="57290e55-335a-4c09-b904-a795572d6cda",
            code="CS1101S",
            name="Programming Methodology",
            teaching=True,
            term="1820",
        )

        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            module = Module.from_api(api_data)
        self.assertEqual(module, expected_module)
        self.assertIsNone(Module.from_api({}))

    def test_get_lesssons(self):
        module_id = "9db79e1f-4b15-4fe9-8783-363990eeff09"
        test_module = Module(
                id='9db79e1f-4b15-4fe9-8783-363990eeff09',
                code='CS4261/CS5461',
                name='Algorithmic Mechanism Design',
                teaching=False,
                term='1910',
        )
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
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            lessons = test_module.lessons(authorization)

        # lessons = result.data
        self.assertEqual(len(lessons), len(expected_lessons))
        for lesson1, lesson2 in zip(lessons, expected_lessons):
            self.assertEqual(lesson1, lesson2)

    def test_announcements(self):
        self.maxDiff = None
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            announcements = module.announcements(authorization)
        expected_announcements = [
            {
                "description": "Dear All,\n\n \n\nThe midterm seating plan is now uploaded in the folder lecture_notes.\n\n \n\nKind Regards,\n\n \n\nA/P Ajay Jasra\n",
                "title": "Mid Term Seating Plan",
                "datetime": parse("2019-03-07 05:29:02.847Z"),
            },
            {
                "description": "Dear All,\n\n \n\nThese have been added to `lecture notes'. I will quickly cover how to use these in our next lecture.\n\n \n\nKind Regards,\n\n \n\nA/P Ajay Jasra\n",
                "title": "Gaussian CDF and Quantile Tables",
                "datetime": parse("2019-02-26 03:44:37.287Z"),
            },
            {
                "description": "Date/Time/Venue\nThe mid-semester test will be held on 12th Mar, Tuesday from 2000hrs to 2100 hrs in MPSH2.\n\nTest details\nScope of test -- Chapters: 1 to 2\n\nSeveral multiple choice questions and some short questions, attempt all. Duration: 60 mins.\n \nOthers\nYou are allowed to bring along with you ONE piece of A4 size, two-sided help sheet.\nProgrammable/graphical/scientific calculators are allowed.\n \nMake-up test Policy\nIf you miss the test due to illness, you will be allowed to take a make-up test provided you have a valid medical certificate for the day of test.\nContact me within 24 hrs after the test.\n\nYou will be notified of the details of the make-up test (to be held during week 13) via your NUS email.\n \nShould for any other reason you are not able to take the test, contact me ahead of time before the test (if it is possible). Legitimate reasons include:\n\n\n\tBereavement of immediate family member and burial or cremation takes place on same day and time as test;\n\tStudent is affected by serious trauma caused by crime, accidents or disasters (e.g. fire);\n\tStudent is officially representing the country in an official international competition in which the student has no control over the actual dates of the competition; and\n\tStudent is representing NUS at NUS-recognised University-level competitions, i.e. Universiade (World University Games), AseanUniversity Games and IndianRimAsianUniversity Games (IRAUG).\n\tInvolvement in University level performances. i.e. concerts, plays.\n\n\nNote that Hall activities or driving tests are not considered valid non-medical reasons for missing CA tests.\n",
                "title": "Mid Term",
                "datetime": parse("2019-02-14 07:49:49.227Z"),
            },
        ]
        self.assertEqual(len(expected_announcements), len(announcements))
        for a1, a2 in zip(expected_announcements, announcements):
            # NOTE annoying to match the entire description text due to the html
            # parsing library differs to platform
            self.assertEqual(a1["datetime"], a2["datetime"])
            self.assertEqual(a1["title"], a2["title"])
            self.assertEqual(a1["description"][:5], a2["description"][:5])

    def test_announcements_archived(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            announcements = module.announcements(authorization, archived=True)
        self.assertEqual([], announcements)
