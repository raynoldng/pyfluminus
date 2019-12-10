from __future__ import annotations
from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL

# from pyfluminus.structs import Module
from pyfluminus import utils
from pyfluminus.constants import ErrorTypes

import requests
import urllib.parse as parse
import json

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyfluminus.structs import Module, File

teaching_perms = [
    "access_Full",
    "access_Create",
    "access_Update",
    "access_Delete",
    "access_Settings_Read",
    "access_Settings_Update",
]


class Result:
    """contains the response from API calls"""

    def __init__(self, data=None, error_type=None, error_msg=None):
        self.data = data
        self.error_type = error_type
        self.error_msg = error_msg

    def okay(self):
        return self.data is not None


class ErrorResult(Result):
    """convenience wrapper for initializing Error results"""

    def __init__(self, error_type=None, error_msg=None):
        super().__init__(data=None, error_type=error_type, error_msg=error_msg)


def name(auth: Dict) -> Result:
    response = api(auth, "user/Profile")
    if "userNameOriginal" in response:
        name = response["userNameOriginal"].title()
        return Result(data=name)
    return ErrorResult(error_type=ErrorTypes.Error)


def current_term(auth: Dict) -> Result:
    """returns info about current term
    e.g.: {term: "1820", description: "2018/2019 Semester 2"}
    """
    response = api(auth, "/setting/AcademicWeek/current?populate=termDetail")
    if "termDetail" in response:
        return Result({
            "term": response["termDetail"]["term"],
            "description": response["termDetail"]["description"],
        })
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


def modules(auth: Dict, current_term_only: bool = False) -> Result:
    """ returns list of modules that user with given authorization is reading
    """
    from pyfluminus.structs import Module

    response = api(auth, "module")
    if "data" in response:
        return Result([
            Module(
                id=mod["id"],
                code=mod["name"],
                name=mod["courseName"],
                teaching=any(mod["access"].get(perm, False) for perm in teaching_perms),
                term=mod["term"],
            )
            for mod in response["data"]
        ])
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


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
