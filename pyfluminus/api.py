from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL
from pyfluminus.structs import Module

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
    "access_Settings_Updat",
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
    response = api(auth, "/module")
    if "data" in response:
        return [
            Module(
                id=mod["id"],
                code=mod["name"],
                name=mod["courseName"],
                teaching=any(mod["access"].get(perm, False) for perm in teaching_perms),
                term=mod['term'],
            )
            for mod in response["data"]
        ]
    return {"error": {"unexpected_response": response}}


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
    uri = parse.urljoin(API_BASE_URL, path)
    method = requests.get if method == "get" else requests.post

    response = method(uri, headers=headers, data=data)

    status_code = response.status_code
    if status_code == 200:
        return json.loads(response.content)
    elif status_code == 401:
        return {"error": "expired token"}
    return {"error": response.content}
