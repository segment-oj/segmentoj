# tools
import re

def isEmail(str):
	p = re.compile("^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$")

	if p.match(str):
		return True
	else:
		return False