import unittest
from unittest.mock import patch
import os, shutil

from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

from pyfluminus.tests.mock_server import MOCK_CONSTANTS
from pyfluminus.structs import Module, File
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
sample_file = File(
    id="731db9ba-b919-4614-928c-1ac7d4172b3c",
    name="Jasra, Ajay - Tut1.docx",
    directory=False,
    children=None,
    allow_upload=False,
    multimedia=False,
)


class TestFile(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            print("removed test generated files")
            shutil.rmtree(temp_dir)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            print("removed test generated files")
            shutil.rmtree(temp_dir)

    def test_files_from_module(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            file = File.from_module(authorization, module)
        expected_file = File(
            id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",  # id of ST2334
            name="ST2334",
            directory=True,
            children=[
                File(
                    id="7c464b62-3811-4c87-b1d1-7407e6ec321b",
                    name="Tutorial Questions",
                    directory=True,
                    children=None,
                    allow_upload=False,
                    multimedia=False,
                ),
                File(
                    id="5a9525ba-e90c-44aa-a659-267bbf508d11",
                    name="Lecture Notes",
                    directory=True,
                    children=None,
                    allow_upload=False,
                    multimedia=False,
                ),
            ],
            allow_upload=False,
            multimedia=False,
        )
        self.assertEqual(expected_file, file)

    def test_file_from_module_filename_sanitised(self):
        # ignore the fields other than code are wrong
        module = Module(
            code="CS1231/MA1100",
            id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",
            name="Probability and Statistics",
            teaching=False,
            term="1820",
        )

        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            file = File.from_module(authorization, module)
        self.assertEquals(file.name, "CS1231-MA1100")

    def test_load_children_directory_allow_upload_prepends_creators_name(self):
        expected_children = [
            File(
                id="399c60ce-26a9-4567-9864-83a7964c60d3",
                name="Jasra, Ajay - ST2334 Solution to Tut 5.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="6d2c2c56-0ee5-4f63-a56d-2c5b64565ff5",
                name="Jasra, Ajay - ST2334 Solution to Tut 4.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="64904b93-cc80-4397-b085-122852b711b1",
                name="Jasra, Ajay - ST2334 Solution to Tut 3.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="e9109d02-4054-4c5c-ae94-264e424fd525",
                name="Jasra, Ajay - ST2334 Solution to Tut 2.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="e5014221-6e1d-4907-a0e0-1ce6a30a67da",
                name="Jasra, Ajay - ST2334 Solution to Tut 1.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="566fcc1a-d5e2-4e9d-b53d-b12f25ec37ee",
                name="Jasra, Ajay - Tut11.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="361d6f87-f2ca-499f-9c61-1c200baed725",
                name="Jasra, Ajay - Tut10.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="bb9a448d-4757-4767-bd8d-2fc1220224bf",
                name="Jasra, Ajay - Tut9.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="ad3f5277-f9d0-4c9f-8283-04d4b2ce986a",
                name="Jasra, Ajay - Tut8.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="2dd73690-b6ee-47cd-99d5-b486fb3cb513",
                name="Jasra, Ajay - Tut6.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="b8889d6d-3a38-4404-ac0f-aa53799a5237",
                name="Jasra, Ajay - Tut7.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="dbc6c7fd-0261-4603-b233-beca395067fa",
                name="Jasra, Ajay - Tut4.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="8ae29e68-822b-471b-866b-9b1098fcede2",
                name="Jasra, Ajay - Tut5.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="d3009c67-f037-484e-bcab-3028f9a321da",
                name="Jasra, Ajay - Tut2.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="08905bc1-de56-4c5e-9620-7dacf0cca377",
                name="Jasra, Ajay - Tut3.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="731db9ba-b919-4614-928c-1ac7d4172b3c",
                name="Jasra, Ajay - Tut1.docx",
                directory=False,
                children=[],
                allow_upload=False,
                multimedia=False,
            ),
        ]

        file = File(
            id="7c464b62-3811-4c87-b1d1-7407e6ec321b",
            name="Tutorial Questions",
            directory=True,
            children=None,
            allow_upload=True,
            multimedia=False,
        )
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = file.load_children(authorization)

        self.assertTrue(result.ok)
        self.assertEqual(len(expected_children), len(file.children))
        for child1, child2 in zip(expected_children, file.children):
            self.assertEqual(child1, child2, "{}\n{}".format(child1, child2))

    def test_load_children_directory(self):
        file = File(
            id="40582141-1a1d-41b6-ba3a-efa44ff7fd05",
            name="ST2334",
            directory=True,
            children=None,
            allow_upload=False,
            multimedia=False,
        )
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result = file.load_children(authorization)

        self.assertTrue(result.ok)
        expected_childen = [
            File(
                id="7c464b62-3811-4c87-b1d1-7407e6ec321b",
                name="Tutorial Questions",
                directory=True,
                children=None,
                allow_upload=False,
                multimedia=False,
            ),
            File(
                id="5a9525ba-e90c-44aa-a659-267bbf508d11",
                name="Lecture Notes",
                directory=True,
                children=None,
                allow_upload=False,
                multimedia=False,
            ),
        ]
        self.assertEqual(len(expected_childen), len(file.children))
        for child1, child2 in zip(expected_childen, file.children):
            self.assertEqual(child1, child2, "{}\n{}".format(child1, child2))

    def test_load_children_file(self):
        file = File(
            id="731db9ba-b919-4614-928c-1ac7d4172b3c",
            name="Tut1.docx",
            directory=False,
            children=None,
            allow_upload=False,
            multimedia=False,
        )
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result1 = file.load_children(authorization)
        self.assertTrue(result1.ok)
        self.assertListEqual([], file.children)

        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result2 = file.load_children(authorization)
        self.assertTrue(result2.ok)
        self.assertListEqual([], file.children)

    def test_get_download_url(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            download_url = sample_file.get_download_url(authorization)
        self.assertEqual(
            download_url,
            "http://localhost:8082/v2/api/files/download/6f3cfb8c-5b91-4d5a-849a-70dcb31eea87",
        )

    def test_download(self):
        with patch.dict("pyfluminus.api.__dict__", MOCK_CONSTANTS):
            result1 = sample_file.download(authorization, temp_dir)
            expected_filepath = os.path.join(temp_dir, sample_file.name)
            self.assertTrue(result1.ok)
            self.assertTrue(
                os.path.exists(expected_filepath),
                "cannnot find file {}".format(expected_filepath),
            )
            with open(expected_filepath, "r") as f:
                self.assertEqual(
                    "This is just a sample file.\n", "".join(f.readlines())
                )
            result2 = sample_file.download(authorization, temp_dir)
            self.assertFalse(result2.ok)
            self.assertEquals(result2.error_type, ErrorTypes.FileExists)

