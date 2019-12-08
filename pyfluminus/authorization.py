from typing import Dict
import requests
import urllib.parse as parse
import json


from pyfluminus.constants import AUTH_URL, CLIENT_ID, REDIRECT_URI, RESOURCE


def vafs_jwt(username: str, password: str) -> Dict:
    """return jwt from openID authentication
    username -- username of NUSNET account (e.g. nusstu\e00123123)
    password -- password of NUSNET account 

    returns jwt token (str) or error message if fail
    """
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "resource": RESOURCE,
    }

    auth_data = {
        "UserName": username,
        "Password": password,
        "AuthMethod": "FormsAuthentication",
    }

    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    url = AUTH_URL + "?" + parse.urlencode(auth_params)
    response = requests.post(url, headers=auth_headers, data=auth_data)

    if len(response.history) != 2:
        return {"error": "invalid credentials"}

    resp1, resp2 = response.history

    # get the code found in the query parameters of
    # the location header of second response
    decoded = parse.urlparse(resp2.headers["Location"])
    code = dict(parse.parse_qsl(decoded.query))["code"]

    adfs_body = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    api_base_url = "https://luminus.nus.edu.sg/v2/api/"
    api_login_url = api_base_url + "login/adfstoken"

    login_headers = {
        "Ocp-Apim-Subscription-Key": "6963c200ca9440de8fa1eede730d8f7e",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    token_resp = requests.post(url=api_login_url, data=adfs_body, headers=login_headers)
    access_token = json.loads(token_resp.text).get("access_token")

    return {"jwt": access_token}

