import struct
import datetime

class ThermostatData:
	format =  ">" # big endian
	format += "I" # unsigned int, 4 bytes, always 0x12 in the data, seemingly the same across updates too
	format += "Q" # unsigned long long, 8 bytes (64 bits), looks like a time
	format += "I" # unsigned int, 4 bytes, always 0x6 in the data, seemingly the same across updates too
	format += "I" # unsigned int, 4 bytes

	def __init__(self, a, time, c, cmp_spd, raw_data=[]):
		self.a = a
		self.time = time
		self.c = c
		self.cmp_spd = cmp_spd
		self.raw_data = raw_data

	@classmethod
	def from_data(cls, data:bytes):
		a, time, c, cmp_spd = struct.unpack(cls.format, data)
		return cls(a, time, c, cmp_spd, raw_data=data)

	def __str__(self):
		return "ThermostatData<a: " + str(self.a) + ", time: " + datetime.datetime.fromtimestamp(self.time).isoformat() + ", c: " + str(self.c) + ", cmp_spd: " + str(self.cmp_spd) + "% >" 


