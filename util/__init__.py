import os
import re
from base64 import b64encode, urlsafe_b64encode

base64 = lambda s: b64encode(s.encode()).decode()
random_token = lambda: urlsafe_b64encode(os.urandom(16)).decode()

def prompt(msg, regex='.*', default=None, readFile=False):
    result = input(msg)
    if not result and default:
        return default
    if not re.match(regex, result):
        raise ValueError(f"expect response to match the regex '{regex}'.")
    if readFile:
        with open(result, 'r') as file:
            data=file.read()
        return data
    else:
        return result
