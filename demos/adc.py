# -*- coding: utf-8 -*-

from smbus import SMBus
from time import sleep

# ACHTUNG: Das SMBus-Protokoll geht bei der Übertragung von Werten mit
# mehr als einem Byte Länge (16-bit-Word) davon aus, dass das LSB zuerst
# übertragen wird. Der ADS1015 sendet jedoch das MSB zuerst, daher ist
# eine Konvertierung notwendig

def swap_bytes_16bit(value):
	return ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)

class ADC:
	__CONFIG_REGISTER     = 0b01
	__CONVERSION_REGISTER = 0b00

	__CONFIG_MUX_BITS = 0b0111000000000000
	# Bits zur Konfiguration des Muxers zum Messen von Spannungen relativ
	# zu Masse, für Eingänge A1 bis A4
	__CONFIG_MUX_ABSOLUTE = [
		0b0100000000000000,
		0b0101000000000000,
		0b0110000000000000,
		0b0111000000000000 ]

	__CONFIG_PGA_BITS   = 0b0000111000000000
	__CONFIG_PGA_4_VOLT = 0b0000001000000000

	__CONFIG_MODE_BITS       = 0b0000000100000000
	__CONFIG_MODE_CONTINUOUS = 0
	
	def __init__(self, bus, bus_address = 0x49):
		self.__bus = bus
		self.__bus_address = bus_address

		config = self.read_config_register()

		config &= ~ADC.__CONFIG_MUX_BITS
		config |=  ADC.__CONFIG_MUX_ABSOLUTE[0]

		config &= ~ADC.__CONFIG_PGA_BITS
		config |=  ADC.__CONFIG_PGA_4_VOLT

		config &= ~ADC.__CONFIG_MODE_BITS
		config |=  ADC.__CONFIG_MODE_CONTINUOUS

		self.write_config_register(config)

	def bus(self):
		return self.__bus

	def bus_address(self):
		return self.__bus_address

	def read_config_register(self):
		config = self.__bus.read_word_data(self.__bus_address, ADC.__CONFIG_REGISTER)
		return swap_bytes_16bit(config)

	def write_config_register(self, configuration):
		"""
		:type configuration: 16-bit word
		"""
		self.__bus.write_word_data(self.__bus_address, ADC.__CONFIG_REGISTER, swap_bytes_16bit(configuration))

	def read_conversion_value(self):
		sensor_value = self.__bus.read_word_data(self.__bus_address, ADC.__CONVERSION_REGISTER)
		sensor_value = swap_bytes_16bit(sensor_value)
		# die niederwertigsten 4 Bit sind immer auf 0 gesetzt, daher können diese
		# ignoriert werden (siehe Datenblatt, Registerbeschreibung Tabelle 8 auf
		# Seite 15)
		return sensor_value >> 4
		

	def set_mux_absolute(self, channel):
		if channel < 0 or channel > 3:
			return
		else:
			config = self.read_config_register()
			config &= ~ADC.__CONFIG_MUX_BITS
			config |= ADC.__CONFIG_MUX_ABSOLUTE[channel]
			self.write_config_register(config)

	def read_channel(self, channel):
		"""
		:param channel: the index of the channel to be read - can be one of [0, 1, 2, 3]
		:returns the converted channel value
		"""
		self.set_mux_absolute(channel)
		# lässt dem ADC Zeit, eine neue Messung mit der neuen
		# Konfiguration stattfinden zu lassen
		sleep(0.001)
		return self.read_conversion_value()

