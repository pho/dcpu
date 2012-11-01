

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
					
try:
	import pygame


	class LEM1802(Device):

		def __init__(self):
			super(LEM1802, self).__init__("LEM1802", 0x7349, 0xf615, 0x1802, 0x1c6c, 0x8b36)
			self.changed = True
			self.lastB = 0
			self.ram = []
			self.disconnected = True
			for i in range(384):
				self.ram.append(0x0) # CELLS?

			pygame.init()
			self.size = (320, 240)
			self.screen = pygame.display.set_mode(self.size)
		
		def render(self):
			if self.changed:
				for i in range(12):
					for j in range(32):
						rect = pygame.Rect(j*10, i*20, 9, 18)
						(char, B, f, b) = self.decodeColor(self.ram[i+j])
						pygame.draw.rect(self.screen, pygame.Color("#00ff00"), rect)
				pygame.display.flip()
				self.changed = False


		def hwi(self, dcpu):
			A = dcpu.A()

			if A == 0: #MEM_MAP_SCREEN

				B = dcpu.B()
				if B == 0:
					self.lastB = B
					self.disconnected = True
					return

				elif self.lastB == 0:
					self.disconnected = False
					self.lastB = B
					sleep(1)
					#TODO  Other interrupts sent during this time
					#      are still processed.

				for i in range(len(self.ram)):
					#self.ram[i]( dcpu.ram[B+i]() )
					self.ram[i] = dcpu.ram[B+i]()
				self.changes = True

			elif A == 1:
				pass
			elif A == 2:
				pass
			elif A == 3:
				pass
			elif A == 4:
				pass
			elif A == 5:
				pass
		

		def decodeColor(self, i):
			# ffffbbbbBccccccc
			char = i & 0x007f
			B = (i>>7) & 0x1
			b = (i>>8) & 0xf
			f = i>>12

			return (char, B, b, f)



except:
	class LEM1802(Device):

		def __init__(self):
			super(LEM1802, self).__init__("LEM1802", 0x7349, 0xf615, 0x1802, 0x1c6c, 0x8b36)
			self.lastB = 0
			self.ram = []
			self.disconnected = True
			for i in range(384):
				self.ram.append(0x0) # CELLS?

		def hwi(self, dcpu):
			A = dcpu.A()

			if A == 0: #MEM_MAP_SCREEN

				B = dcpu.B()
				if B == 0:
					self.lastB = B
					self.disconnected = True
					return

				elif self.lastB == 0:
					self.disconnected = False
					self.lastB = B
					sleep(1)
					#TODO  Other interrupts sent during this time
					#      are still processed.

				for i in range(len(self.ram)):
					#self.ram[i]( dcpu.ram[B+i]() )
					self.ram[i] = dcpu.ram[B+i]()

			elif A == 1:
				pass
			elif A == 2:
				pass
			elif A == 3:
				pass
			elif A == 4:
				pass
			elif A == 5:
				pass
		

		def decodeColor(self, i):
			# ffffbbbbBccccccc
			char = i & 0x007f
			B = (i>>7) & 0x1
			b = (i>>8) & 0xf
			f = i>>12

			return (char, B, b, f)

