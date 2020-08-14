# generating captcha

from django.utils import timezone
import datetime
import random
import math
from PIL import Image, ImageDraw, ImageFont

from .apps import CaptchaConfig

class GenCaptcha:
    
    def __init__(self):
        self.height = CaptchaConfig.picture_height
        self.width = CaptchaConfig.picture_width
        self.length = CaptchaConfig.length

        self.fontsize = CaptchaConfig.font_size
        self.fonttype = CaptchaConfig.font_family

        self.dot_number = CaptchaConfig.dot_number
        self.line_number = CaptchaConfig.line_number

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

        while random_lower == 'o':
            random_lower = chr(random.randint(97, 122))
        while random_upper == 'O':
            random_upper = chr(random.randint(65, 90))

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

    def checkSimilarity(self, color1, color2):
        r1 = color1[0]
        g1 = color1[1]
        b1 = color1[2]

        r2 = color2[0]
        g2 = color2[1]
        b2 = color2[2]

        r3 = (r1 - r2) / 256
        g3 = (g1 - g2) / 256
        b3 = (b1 - b2) / 256

        color_diff = math.sqrt(r3 ** 2 + g3 ** 2 + b3 ** 2)

        bright1 = ((r1 * 299) + (g1 * 587) + (b1 * 114))
        bright2 = ((r2 * 299) + (g2 * 587) + (b2 * 114))

        bright_diff = abs(bright1 - bright2)

        if color_diff < 0.7 or bright_diff < 100 * 255:
            return True
        return False

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
            while self.checkSimilarity(bg_color, txt_color):
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

def settimelater(d=-CaptchaConfig.age):

    nowtime = timezone.now()
    res = nowtime + datetime.timedelta(minutes=5)
    return res
