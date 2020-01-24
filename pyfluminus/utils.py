"""
A collection of common methods in fluminus
"""
import re
import requests
import shutil
import sys, os
from bs4 import BeautifulSoup

from pyfluminus.api_structs import Result, ErrorResult, EmptyResult
from pyfluminus.constants import ErrorTypes


def sanitise_filename(name: str, replacement="-") -> str:
    return re.sub(r"[\/\0]", replacement, name)


def download(url: str, destination: str, verbose: bool) -> Result:
    # TODO verbose currently doesnt do anything
    if os.path.isfile(destination):
        return ErrorResult(ErrorTypes.FileExists)

    # if directory does not exist then create it
    dir_path = os.path.dirname(destination)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with requests.get(url, allow_redirects=True, stream=True) as r:
        with open(destination, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return EmptyResult()

def download_w_session(session, url: str, destination: str, verbose: bool) -> Result:
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

    with session.get(url, allow_redirects=True, stream=True) as r:
        with open(destination, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return EmptyResult()


def remove_html_tags(html_text: str) -> str:
    return BeautifulSoup(html_text, features="lxml").get_text()

