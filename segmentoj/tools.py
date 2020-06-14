# tools
import re, markdown, html

def isEmail(str):
	p = re.compile(r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$")

	if p.match(str):
		return True
	else:
		return False

def markdown2html(str, allowhtml = False):
	if not allowhtml:
		str = html.escape(str)
	
	str = markdown.markdown(
		str,
		extensions=[
        	'markdown.extensions.extra',
        	'markdown.extensions.codehilite',
        ]
	)

	return str