"""
A collection of common methods in fluminus
"""
import re
import requests
import sys, os

def sanitise_filename(name, replacement="-"):
    return re.sub(r'[\/\0]', replacement, name)

def download(url: str, destination: str, verbose: bool):
    # TODO add verbose, for now ignored
    response = requests.get(url, allow_redirects=True)

    # if directory does not exist then create it
    dir_path = os.path.dirname(destination)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with open(destination, 'wb') as f:
        f.write(response.content)