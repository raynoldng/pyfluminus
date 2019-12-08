from pyfluminus.constants import OCP_SUBSCRIPTION_KEY, API_BASE_URL

import requests
import urllib.parse as parse
import json

from typing import Dict


def name(auth: Dict) -> str:
    response = api(auth, 'user/Profile')
    if 'userNameOriginal' in response:
        return response['userNameOriginal'].title()
    return None

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
