from unittest import TestCase

from raspibot import RaspiBot

class TestRaspiBot(TestCase):
    def test_hello(self):
        bot = RaspiBot()
        self.assertEqual(bot.hello(), "Hello")
