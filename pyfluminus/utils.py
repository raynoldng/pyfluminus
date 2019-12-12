"""
A collection of common methods in fluminus
"""
import re
import requests
import sys, os
from bs4 import BeautifulSoup

from pyfluminus.api_structs import Result, ErrorResult
from pyfluminus.constants import ErrorTypes


def sanitise_filename(name, replacement="-"):
    return re.sub(r"[\/\0]", replacement, name)


def download(url: str, destination: str, verbose: bool):
    return download_w_session(requests, destination, url, verbose)


def download_w_session(session, url: str, destination: str, verbose: bool):
    """sessions object needed to download webcasts due to the cookies generating in 
    the video url query used to authenticate download request"""
    # TODO add verbose, for now ignored
    if os.path.isfile(destination):
        return ErrorResult(ErrorTypes.FileExists)

    response = session.get(url, allow_redirects=True)

    # if directory does not exist then create it
    dir_path = os.path.dirname(destination)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with open(destination, "wb") as f:
        f.write(response.content)

    return Result()


def remove_html_tags(html_text):
    # return BeautifulSoup(html_text, features="lxml").get_text().replace(u"\xa0", u" ")
    return BeautifulSoup(html_text, features="lxml").get_text()

