
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
					

class Monitor(Device):

	def hwi(self, dcpu):
		print("IM THE MONITOR LOL")
