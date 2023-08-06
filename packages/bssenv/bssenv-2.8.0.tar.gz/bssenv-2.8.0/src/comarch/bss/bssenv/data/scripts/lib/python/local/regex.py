import re


def is_like(a, regex):
    return bool(re.search(regex, a))
