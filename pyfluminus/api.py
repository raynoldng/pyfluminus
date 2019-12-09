from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL
from pyfluminus.structs import Module, File

import requests
import urllib.parse as parse
import json

from typing import Dict, List


teaching_perms = [
    "access_Full",
    "access_Create",
    "access_Update",
    "access_Delete",
    "access_Settings_Read",
    "access_Settings_Update",
]


def name(auth: Dict) -> str:
    response = api(auth, "user/Profile")
    if "userNameOriginal" in response:
        return response["userNameOriginal"].title()
    return None


def current_term(auth: Dict) -> Dict:
    """returns info about current term
    e.g.: {term: "1820", description: "2018/2019 Semester 2"}
    """
    response = api(auth, "/setting/AcademicWeek/current?populate=termDetail")
    if "termDetail" in response:
        return {
            "term": response["termDetail"]["term"],
            "description": response["termDetail"]["description"],
        }
    return {"error": {"unexpected_response": response}}


def modules(auth: Dict, current_term_only: bool = False) -> List[Module]:
    """ returns list of modules that user with given authorization is reading
    """
    response = api(auth, "module")
    if "data" in response:
        return [
            Module(
                id=mod["id"],
                code=mod["name"],
                name=mod["courseName"],
                teaching=any(mod["access"].get(perm, False) for perm in teaching_perms),
                term=mod["term"],
            )
            for mod in response["data"]
        ]
    return {"error": {"unexpected_response": response}}


def get_file_from_module(auth: Dict, module: Module) -> File:
    return File(
        id=module.id,
        name=module.code,
        directory=True,
        children=get_children(auth, module.id, allow_upload=False),
        allow_upload=False,
        multimedia=False,
    )


def get_children(auth: Dict, id: str, allow_upload: bool) -> List[File]:
    directory_children = api(auth, "files/?ParentID={}".format(id))
    directory_files = api(auth, "files/{}/file".format(id))
    print(directory_children)
    print(directory_files)

    return [
        parse_child(file_data, allow_upload)
        for file_data in directory_children["data"] + directory_files["data"]
    ]


def parse_child(data: Dict, allow_upload: bool) -> File:
    # TODO handle add creator name
    is_directory = isinstance(data.get("access", None), dict)
    return File(
        id=data["id"],
        name=data["name"],
        directory=is_directory,
        children=None if is_directory else [], # NOTE cargo culting logic used in fluminus
        allow_upload=data.get("allowUpload", False),
        multimedia=False,
    )


def api(auth: Dict, path: str, method="get", headers=None, data=None):
    if headers is None:
        headers = dict()
    headers.update(
        {
            "Authorization": "Bearer {}".format(auth["jwt"]),
            "Ocp-Apim-Subscription-Key": OCP_SUBSCRIPTION_KEY,
            "Content-Type": "application/json",
        }
    )
    # NOTE remove leading / else joined url is broken
    uri = parse.urljoin(API_BASE_URL, path.rstrip("/"))
    method = requests.get if method == "get" else requests.post

    response = method(uri, headers=headers, data=data)

    status_code = response.status_code
    if status_code == 200:
        return json.loads(response.content)
    elif status_code == 401:
        return {"error": "expired token"}
    return {"error": response.content}
