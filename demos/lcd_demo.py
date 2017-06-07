# coding: utf-8
from LCD import Display
d = Display()
d.init()
d.clear()
d.print_string("Hallo Leander!")
d.cursor_goto_line(1)
d.print_string("Check' Flosse!")
d.clear()
d.print_string("{0:d} {0:X} {0:b}".format(0xca))
