"""
A collection of common methods in fluminus
"""
import re

def sanitise_filename(name, replacement="-"):
    return re.sub(r'[\/\0]', replacement, name)