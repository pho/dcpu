

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
	import font
	from time import sleep

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
			self.size = (512, 384)
			self.screen = pygame.display.set_mode(self.size)
			self.font = font.font
			self.palette = {
					0  : "#000000",
					1  : "#0000aa",
					2  : "#00aa00",
					3  : "#00aaaa",
					4  : "#aa0000",
					5  : "#aa00aa",
					6  : "#aa5500",
					7  : "#aaaaaa",
					8  : "#555555",
					9  : "#5555ff",
					10 : "#55ff55",
					11 : "#55ffff",
					12 : "#ff5555",
					13 : "#ff55ff",
					14 : "#ffff55",
					16 : "#ffffff"
					}
		
		def render(self):
			#if self.changed:
				for i in range(12):
					for j in range(32):
						(char, B, f, b) = self.decodeColor(self.ram[ (i*32) + j ])
						bg = pygame.Rect(j*16, i*32, 16, 32)
						pygame.draw.rect(self.screen, pygame.Color(self.palette[b]), bg)
						
						for k in range(8):
							for l in range(4):
								if (self.font[( char + 224*(char//32) ) + 32 * k ])>>l&0x1:
										Mc_pixel = pygame.Rect( j*16 + l*4 , i*32 + k*4, 4, 4)
										pygame.draw.rect(self.screen, pygame.Color(self.palette[f]), Mc_pixel)

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

