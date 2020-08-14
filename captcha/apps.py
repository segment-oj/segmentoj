from django.apps import AppConfig
from django.conf import settings

import os.path

class CaptchaConfig(AppConfig):
    name = 'captcha'

    # CAPTCHA settings
    # The height of each captcha pic
    picture_height = 40
    # The width of each captcha pic
    picture_width = 130
    # The length of each captcha pic
    length = 4
    # font size on captcha
    # you may change this if modified height/width
    # try it until you find the best value
    font_size = 30
    # the font file of font
    font_family = os.path.join(settings.BASE_DIR, "captcha", "FiraCode-Regular.ttf")
    # The number of dots on the pic to interfare
    dot_number = 100
    # The number of lines on the pic to interfare
    line_number = 4
    # how long a captcha expire (min)
    age = 5
