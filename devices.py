
class Device:

	def __init__(self, name, id_low, id_high, version, manuf_low, manuf_high):
		self.name = name
		self.id_low = id_low
		self.id_high = id_high
		self.version = version
		self.manuf_low = manuf_low
		self.manuf_high = manuf_high

	def get_info(self):
		return ( self.id_low, self.id_high, self.version, self.manuf_low, self.manuf_high )

	def hwi(self, dcpu):
		pass
					

class LEM1802(Device):

	def __init__(self):
		super(LEM1802, self).__init__("LEM1802", 0x7349, 0xf615, 0x1802, 0x1c6c, 0x8b36)

	def hwi(self, dcpu):
		print("IM THE MONITOR LOL")
		print("DCPU A:{} B:{}".format(hex(dcpu.A()), hex(dcpu.B())))
