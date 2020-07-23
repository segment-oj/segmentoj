# tools
import re, markdown, html


def isEmail(str):
    p = re.compile(r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$")

    if p.match(str):
        return True
    else:
        return False
