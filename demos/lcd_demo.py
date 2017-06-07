"""Demonstrates simple output to the LCD."""

from time import sleep
from LCD import Display

d = Display()
d.init()

d.clear()
d.print_string("Hallo Leander!")
d.cursor_goto_line(1)
d.print_string("Check' Flosse!")

sleep(1.5)

# there is no need for specialized output functions since Python's built-in
# string formatting capabilities are more than sufficient
d.clear()
d.print_string("{0:d} {0:X} {0:b}".format(0xca))
