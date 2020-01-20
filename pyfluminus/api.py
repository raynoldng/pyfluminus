from __future__ import annotations
from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL, ErrorTypes
from pyfluminus import utils
from pyfluminus.api_structs import Result, ErrorResult

import requests
import urllib.parse as parse
import json
from dateutil.parser import parse as date_parse

from typing import Dict, List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pyfluminus.structs import Module, File, Lesson


def name(auth: Dict) -> Result:
    response = api(auth, "user/Profile")["ok"]
    if "userNameOriginal" in response:
        name = response["userNameOriginal"].title()
        return Result(data=name)
    return ErrorResult(error_type=ErrorTypes.Error)


def current_term(auth: Dict) -> Result:
    """returns info about current term
    e.g.: {term: "1820", description: "2018/2019 Semester 2"}
    """
    response = api(auth, "/setting/AcademicWeek/current?populate=termDetail")["ok"]
    if "termDetail" in response:
        return Result(
            {
                "term": response["termDetail"]["term"],
                "description": response["termDetail"]["description"],
            }
        )
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


def modules(auth: Dict, current_term_only: bool = False) -> Result[List[Optional[Module]]]:
    """ returns list of modules that user with given authorization is reading
    """
    from pyfluminus.structs import Module

    response = api(auth, "module")["ok"]
    if "data" in response:
        return Result([Module.from_api(mod_data) for mod_data in response["data"]])
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


def get_announcements(auth: Dict, module_id: str, archive: bool) -> Result:
    fields = ["title", "description", "displayFrom"]
    uri = "announcement/{}/{}?sortby=displayFrom%20ASC".format(
        "Archived" if archive else "NonArchived", module_id
    )
    response = api(auth, uri)["ok"]
    if "data" in response:
        announcements = response["data"]
        result_data = []
        for announcement in response["data"]:
            if not all(key in announcement for key in fields):
                return ErrorResult(ErrorTypes.UnexpectedResponse, response)
            result_data.append(
                {
                    "title": announcement["title"],
                    "description": utils.remove_html_tags(announcement["description"]),
                    "datetime": date_parse(announcement["displayFrom"]),
                }
            )
        return Result(result_data)
    return ErrorResult(ErrorTypes.Error)


def api(auth: Dict, path: str, method="get", headers=None, data=None):
    """luminus API call, returns response content if successful, else an eror dict
    """
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
        try:
            return {"ok": json.loads(response.content)}
        except Exception as e:
            return {"error": e}
    elif status_code == 401:
        return {"error": "expired token"}
    return {"error": response.content}
