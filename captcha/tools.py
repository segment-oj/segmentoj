# generating captcha

from django.conf import settings
import random
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class GenCaptcha:

    def __init__(self):
        CAPTCHA_CONFIG = settings.CAPTCHA
        self.height = CAPTCHA_CONFIG['picture_height']
        self.width = CAPTCHA_CONFIG['picture_width']
        self.length = CAPTCHA_CONFIG['length']

        self.fontsize = CAPTCHA_CONFIG['font_size']
        self.fonttype = CAPTCHA_CONFIG['font_family']

        self.dot_number = CAPTCHA_CONFIG['dot_number']
        self.line_number = CAPTCHA_CONFIG['line_number']

    # generate random color
    # @return -> (r, g, b)
    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    # generate 1 random char (letters & numbers)
    # @return -> one char
    def get_random_char(self):
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
    def draw_line(self, draw):
        for i in range(self.line_number):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.get_random_color())

    # draw random dots to interfere
    # @param -> draw: PIL ImageDraw Object
    # @return -> None
    def draw_point(self, draw):
        for i in range(self.dot_number):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=self.get_random_color())

    def check_similarity(self, color1, color2):
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
    def create_img(self):
        ans = ''

        bg_color = self.get_random_color()

        # create new pic with random background
        img = Image.new(mode='RGB', size=(self.width, self.height), color=bg_color)

        # get ImageDraw object
        draw = ImageDraw.Draw(img)

        # set font with .ttf file
        font = ImageFont.truetype(font=self.fonttype, size=self.fontsize)

        for i in range(self.length):
            # draw text
            random_txt = self.get_random_char()
            txt_color = self.get_random_color()
            # avoid the text color is same to background color
            while self.check_similarity(bg_color, txt_color):
                txt_color = self.get_random_color()

            # draw text
            # I don't quite sure what the numbers is all about under.
            # TODO: fix number under
            draw.text((10 + self.fontsize * i, 3), text=random_txt, fill=txt_color, font=font)

            ans += random_txt

        # draw interfere elements
        self.draw_line(draw)
        self.draw_point(draw)

        buffer = BytesIO()
        img.save(buffer, format='png')
        buffer.seek(0)

        ans = ans.lower()
        return ans, buffer
