# generating captcha

from django.conf import settings
from django.utils import timezone
import datetime
import random
from PIL import Image, ImageDraw, ImageFont

class GenCaptcha:
	
	def __init__(self):
		self.height = settings.CAPTCHA_HEIGHT
		self.width = settings.CAPTCHA_WIDTH
		self.length = settings.CAPTCHA_LENGTH

		self.fontsize = settings.CAPTCHA_FONTSIZE
		self.fonttype = settings.CAPTCHA_FONTTYPE

		self.dot_number = settings.CAPTCHA_DOTNUM
		self.line_number = settings.CAPTCHA_LINENUM

	# generate random color
	# @return -> (r, g, b)
	def getRandomColor(self):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		return (r, g, b)

	# generate 1 random char (letters & numbers)
	# @return -> one char
	def getRandomChar(self):
		random_num = str(random.randint(0, 9))       # numbers
		random_lower = chr(random.randint(97, 122))  # lower case letters
		random_upper = chr(random.randint(65, 90))   # upper case letters 
		random_char = random.choice([random_num, random_lower, random_upper])
		return random_char

	# draw random lines to interfere
	# @param -> draw: PIL ImageDraw Object
	# @return -> None
	def drawLine(self, draw):
		for i in range(self.line_number):
			x1 = random.randint(0, self.width)
			x2 = random.randint(0, self.width)
			y1 = random.randint(0, self.height)
			y2 = random.randint(0, self.height)
			draw.line((x1, y1, x2, y2), fill = self.getRandomColor())
	
	# draw random dots to interfere
	# @param -> draw: PIL ImageDraw Object
	# @return -> None
	def drawPoint(self, draw):
		for i in range(self.dot_number):
			x = random.randint(0, self.width)
			y = random.randint(0, self.height)
			draw.point((x,y), fill = self.getRandomColor())

	# create random picture
	# @param -> img save path
	# @return -> answer
	def createImg(self, path):
		ans = ""

		bg_color = self.getRandomColor()

		# create new pic with random background
		img = Image.new(mode="RGB", size=(self.width, self.height), color=bg_color)
		
		# get ImageDraw object
		draw = ImageDraw.Draw(img)
		
		# set font with .ttf file
		font = ImageFont.truetype(font=self.fonttype, size=self.fontsize)
		
		for i in range(self.length):
			# draw text
			random_txt = self.getRandomChar()
			txt_color = self.getRandomColor()
			# avoid the text color is same to background color
			while txt_color == bg_color:
				txt_color = self.getRandomColor()
			
			# draw text
			# I don't quite sure what the numbers is all about under.
			# TODO: fix number under
			draw.text((10 + 30 * i, 3), text=random_txt, fill=txt_color, font=font)
			
			ans += random_txt

		# draw interfere elements
		self.drawLine(draw)
		self.drawPoint(draw)
		
		with open(path, "wb") as f:
			img.save(f, format="png")

		ans = ans.lower()
		return ans

def settimelater(d = settings.CAPTCHA_AGE):
	nowtime =timezone.now()
	res = nowtime + datetime.timedelta(minutes=5)
	return res
