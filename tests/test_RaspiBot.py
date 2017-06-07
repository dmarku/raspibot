from raspibot import RaspiBot


class TestRaspiBot:
    def test_hello(self):
        bot = RaspiBot()
        assert bot.hello() == 'Hello'

# flake8: noqa