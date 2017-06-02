# RaspiBot Python Package

A Python Package to control the RoboSchool's RaspiBot robot.

For now, this package will support **Python 3 only**.

## Installation

You can install the package with pip:

```
pip3 install git+https://github.com/tuc-roboschool/raspibot.git
```

## Usage

```.py
from raspibot import RaspiBot

bot = RaspiBot()

print(bot.hello())
# => 'Hello'
```

## Developing

### Installation

For development, it's convenient to have the sources available locally and
install the package in editable mode, so that every change to the sources is
reflected in all following imports.

```
git clone https://github.com/tuc-roboschool/raspibot.git
cd raspibot
pip3 install --user --editable .
```

### Running the Tests

To run the tests, use nose

```
pip3 install nose
nosetests
```

(from http://python-packaging.readthedocs.io/en/latest/testing.html)


### Contributing

If you want to contribute to the project, you can [open issues on Github](https://github.com/tuc-roboschool/raspibot/issues) or fork the project and open a pull request.
