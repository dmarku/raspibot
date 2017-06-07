#!/usr/bin/env python
# -*- coding: utf-8 -*-

from adc import ADC
from smbus import SMBus
from time import sleep

bus = SMBus(1)
adc = ADC(bus)

# Kontinuierliche Ausgabe der Sensorwerte auf der Standardausgabe, bis das
# Programm mit Strg+C beendet wird
try:
	while True:
		left, right = adc.read_channel(0), adc.read_channel(1)
		print("{0:>5d} {1:>5d}".format(left, right))
		sleep(0.2)
except KeyboardInterrupt:
	print('Bye')
