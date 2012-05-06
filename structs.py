import sys

class Register:
	def __init__(self):
		self.value = 0x0000

	def __call__(self):
		return self.value

	def __set__(self, a):
		self.value = a

class DCPU:

	def SET(self, a, b):
		print("SET", hex(a), hex(b))
		v1 = resolve(a)
		v2 = resolve(b)

		self.ram[v1] = v2
		self.PCpp

	def ADD(self, a, b):
		print("ADD", hex(a), hex(b))
		if a == 0xffff:
			O = 0x0001
		else:
			O = 0x0000
		self.ram[a] = (self.ram[a] + b) % 0xffff

	def SUB(self, a, b):
		print("SUB")

	def MUL(self, a, b):
		print("MUL")

	def DIV(self, a, b):
		print("DIV")

	def MOD(self, a, b):
		print("MOD")

	def SHL(self, a, b):
		print("SHL")

	def SHR(self, a, b):
		print("SHR")

	def AND(self, a, b):
		print("AND")

	def BOR(self, a, b):
		print("BOR")

	def XOR(self, a, b):
		print("XOR")

	def IFE(self, a, b):
		print("IFE")

	def IFN(self, a, b):
		print("IFN")

	def IFG(self, a, b):
		print("IFG")

	def IFB(self, a, b):
		print("IFB")

	def JSR(self, a):
		print("JSR", a)

	def __init__(self):
		self.ram = [0x0000] * 65535
		self.A, self.B, self.C, self.X, self.Y, self.Z, self.I, self.J = \
			0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000

		self.PC, self.SP, self.O = \
			0x0000,0x0000,0x0000


		
		self.opcodes = { 0x0 : self.nonbasic,
					0x1 : self.SET,
					0x2	: self.ADD,
					0x3 : self.SUB,
					0x4 : self.MUL,
					0x5 : self.DIV,
					0x6 : self.MOD,
					0x7 : self.SHL,
					0x8 : self.SHR,
					0x9 : self.AND,
					0xa : self.BOR,
					0xb : self.XOR,
					0xc : self.IFE,
					0xd : self.IFN,
					0xe : self.IFG,
					0xf : self.IFB
					}



		self.nbopcodes = {
						0x01 : self.JSR,
					}



		self.values = {
				0x00 : self.A,
				0x01 : self.B,
				0x02 : self.C,
				0x03 : self.X,
				0x04 : self.Y,
				0x05 : self.Z,
				0x06 : self.I,
				0x07 : self.J,
				0x08 : self.ram[self.A],
				0x09 : self.ram[self.B],
				0x0a : self.ram[self.C],
				0x0b : self.ram[self.X],
				0x0c : self.ram[self.Y],
				0x0c : self.ram[self.Z],
				0x0e : self.ram[self.I],
				0x0f : self.ram[self.J],
				#TODO
				0x18 : self.POP,
				0x19 : self.ramSP,
				0x1a : self.PUSH,
				0x1b : self.SP,
				0x1c : self.PC,
				0x1d : self.O,
				0x1e : self.ramPCpp,
				0x1f : self.PCpp
				#TODO
				}


	def nonbasic(self, o, a):
		print("NONBASIC", hex(a))
		try:
			self.nbopcodes[o](a)
		except (KeyError):
			if o >= 0x02 and o <=0x3f:
					print("RESERVED OPCODE:", hex(o))
			else:
					print("OPCODE DOESNT EXISTS:", hex(o))

	def POP(self):
		self.SP += 0x0001
		return self.ram[self.SP]

	def PUSH(self, v):
		self.ram[self.SP] = v
		self.SP -= 0x0001
		return self.ram[self.SP]

	def PCpp(self):
		self.PC += 0x0001
		return self.PC
		
	def ramSP(self):
		return self.ram[self.SP]

	def ramPCpp(self):
		self.PCpp()
		return self.ram[self.PC]


####
	def resolve(self, a):
		if a > 0x18:
			return a()
		else:
			return a

	def decode(self, i):
		opcode = i & 0x000f
		a = (i>>4) & 0x3f
		b = i>>10

		return (opcode, a, b)

	def ejec(self, i):
		(o, a, b) = self.decode(i)
		print "OPCODE:", hex(o)
		self.opcodes[o](a, b)

	def dumpmem(self):
		length = 80 #len(self.ram)
		for i in range(0, length, 8):
			print hex(i),":",
			for j in range(0, 8):
				 print hex(self.ram[i+j]),
			print

	#TODO
	def setram(buf):
		pass
	def setPC(add):
		pass

cpu = DCPU()
if len(sys.argv) > 1:
	ins = sys.argv[1:]
else:
	ins = [0x0411, 0x0412]
for i in ins:
	print "Parametro:", i
	cpu.ejec(int(str(i), 16))
cpu.dumpmem()
	

