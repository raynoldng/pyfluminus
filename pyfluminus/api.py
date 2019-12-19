from __future__ import annotations
from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL, ErrorTypes
from pyfluminus import utils
from pyfluminus.api_structs import Result, ErrorResult

import requests
import urllib.parse as parse
import json
from dateutil.parser import parse as date_parse

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyfluminus.structs import Module, File, Lesson


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
        return Result(
            {
                "term": response["termDetail"]["term"],
                "description": response["termDetail"]["description"],
            }
        )
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


def modules(auth: Dict, current_term_only: bool = False) -> Result:
    """ returns list of modules that user with given authorization is reading
    """
    from pyfluminus.structs import Module

    response = api(auth, "module")
    if "data" in response:
        return Result([Module.from_api(mod_data) for mod_data in response["data"]])
    return ErrorResult(ErrorTypes.UnexpectedResponse, response)


def get_announcements(auth: Dict, module_id: str, archive: bool) -> Result:
    fields = ["title", "description", "displayFrom"]
    uri = "/announcement/{}/{}?sortby=displayFrom%20ASC".format(
        "Archived" if archive else "NonArchived", module_id
    )
    response = api(auth, uri)
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


def get_lessons(auth: Dict, module_id: str) -> Result:
    from pyfluminus.structs import Lesson

    uri = "/lessonplan/Lesson/?ModuleID={}".format(module_id)
    response = api(auth, uri)
    if "data" in response:
        return Result(
            [
                Lesson.from_api(lesson_data, module_id)
                for lesson_data in response["data"]
            ]
        )
    return ErrorResult(ErrorTypes.Error)


def get_files_from_lesson(auth: Dict, lesson: Lesson) -> Result:
    from pyfluminus.structs import File

    uri = "/lessonplan/Activity/?populate=TargetAncestor&ModuleID={}&LessonID={}".format(
        lesson.module_id, lesson.id
    )
    response = api(auth, uri)
    if "data" in response:
        files = [File.from_lesson(file_data) for file_data in response["data"]]
        return Result([f for f in files if f is not None])
    return ErrorResult(ErrorTypes.Error)


def get_weblectures(auth: Dict, module_id: str) -> Result:
    from pyfluminus.structs import Weblecture
    uri_parent = "weblecture/?ParentID={}".format(module_id)
    parent_result = api(auth, uri_parent)
    if "error" in parent_result:
        return ErrorResult()
    uri_children = "weblecture/{}/sessions/?sortby=createdDate".format(
        parent_result["id"]
    )
    children_result = api(auth, uri_children)
    if not "data" in children_result:
        return ErrorResult()
    return Result(
        [Weblecture.from_api(item, module_id) for item in children_result['data']]
    ) if isinstance(children_result['data'], list) else ErrorResult()

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
        return json.loads(response.content)
    elif status_code == 401:
        return {"error": "expired token"}
    return {"error": response.content}
