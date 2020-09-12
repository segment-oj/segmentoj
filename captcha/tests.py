from django.test import TestCase
from captcha.tools import GenCaptcha

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from .views import getcaptcha

import random

# Create your tests here.


class GenCaptchaTest(TestCase):
    # set up test
    def setUp(self):
        self.captcha = GenCaptcha()

    def testZ_get_random_color(self):
        for i in range(1, 1000):
            color = self.captcha.getRandomColor()

            r = color[0]
            g = color[1]
            b = color[2]

            r_in_range = r >= 0 and r <= 255
            g_in_range = g >= 0 and g <= 255
            b_in_range = b >= 0 and b <= 255

            resault = r_in_range and g_in_range and b_in_range

            self.assertTrue(resault)

    def testY_get_random_char(self):
        for i in range(1, 1000):
            random_char = self.captcha.getRandomChar()

            is_number = random_char >= "0" and random_char <= "9"
            is_upper = random_char >= "A" and random_char <= "Z"
            is_lower = random_char >= "a" and random_char <= "z"

            is_char = is_number or is_lower or is_upper

            is_o = random_char == 'o' or random_char == 'O'

            resault = is_char and not is_o

            self.assertTrue(resault)

    def testX_check_similarity_false_far(self):
        color1 = (0, 0, 0)
        color2 = (255, 255, 255)

        self.assertFalse(self.captcha.checkSimilarity(color1, color2))

    def testW_check_similarity_false_close(self):
        color1 = (249, 244, 217)
        color2 = (69, 157, 245)

        self.assertFalse(self.captcha.checkSimilarity(color1, color2))

    def testV_check_similarity_same(self):
        color = (56, 1, 31)

        self.assertTrue(self.captcha.checkSimilarity(color, color))

    def testU_check_similarity_true(self):
        color1 = (69, 157, 245)
        color2 = (70, 158, 246)

        self.assertTrue(self.captcha.checkSimilarity(color1, color2))


class CaptchaViewTest(TestCase):
    # set up test
    def setUp(self):
        self.base_url = "/api/captch/{captcha_key}?sfid={random_number}"
        self.factory = APIRequestFactory()

    def testZ_get_catpcha(self):
        random_key = random.randrange(1, 2000000000)

        request = self.factory.get(self.base_url.format(
            captcha_key=random_key, random_number=random.random()))
        response = getcaptcha(request, key=random_key)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def testY_get_captcha(self):
        random_key = "HACK"

        request = self.factory.get(self.base_url.format(
            captcha_key=random_key, random_number=random.random()))
        response = getcaptcha(request, key=random_key)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
