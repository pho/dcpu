import sys, types

class DCPU:

	def SET(self, a, b):
		print("SET", hex(a), hex(b))
		v1 = self.resolve(a)
		v2 = self.resolve(b)

		self.ram[v1] = v2
		self.PCpp

	def ADD(self, a, b):
		print("ADD", hex(a), hex(b))
		if a == 0xffff:
			EX = 0x0001
		else:
			EX = 0x0000
		self.ram[a] = (self.ram[a] + b) % 0xffff

	def SUB(self, a, b):
		print("SUB")
	
	def MUL(self, a, b):
		print("MUL")

	def MLI(self, a, b):
		print("MLI")

	def DIV(self, a, b):
		print("DIV")

	def DVI(self, a, b):
		print("DVI")

	def MOD(self, a, b):
		print("MOD")

	def MDI(self, a, b):
		print("DIV")

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

	def IFL(self, a, b):
		print("IFL")

	def IFA(self, a, b):
		print("IFA")

	def IFN(self, a, b):
		print("IFN")

	def IFU(self, a, b):
		print("IFU")

	def IFG(self, a, b):
		print("IFG")

	def IFB(self, a, b):
		print("IFB")

	def ADX(self, a, b):
		print("ADX")

	def ASR(self, a, b):
		print("ASR")

	def IFC(self, a, b):
		print("IFC")

	def SBX(self, a, b):
		print("IFC")
	
	def STI(self, a, b):
		print("IFC")

	def STD(self, a, b):
		print("IFC")

## SOPCODES

	def INT(self, a, b):
		print("IFC")

	def IAG(self, a, b):
		print("IFC")

	def IAS(self, a, b):
		print("IFC")

	def RFI(self, a, b):
		print("IFC")

	def IAQ(self, a, b):
		print("IFC")

	def HWN(self, a):
		print("JSR", a)

	def HWQ(self, a):
		print("JSR", a)

	def HWI(self, a):
		print("JSR", a)

	def JSR(self, a):
		print("JSR", a)



## 
	def __init__(self):
		self.ram = [0x0000] * 65535
		self.A, self.B, self.C, self.X, self.Y, self.Z, self.I, self.J = \
			0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000

		self.PC, self.SP, self.EX, self.IA = \
			0x0000,0x0000,0x0000, 0x0000


		
		self.opcodes = {0x0 : self.sopcode,
						0x1 : self.SET,
						0x2 : self.ADD,
						0x3 : self.SUB,
						0x4 : self.MUL,
						0x5 : self.MLI,
						0x6 : self.DIV,
						0x7 : self.DVI,
						0x8 : self.MOD,
						0x9 : self.MDI,
						0xa : self.AND,
						0xb : self.BOR,
						0xc : self.XOR,
						0xd : self.SHR,
						0xe : self.ASR,
						0xf : self.SHL,
						0x10: self.IFB,
						0x11: self.IFC,
						0x12: self.IFE,
						0x13: self.IFN,
						0x14: self.IFG,
						0x15: self.IFA,
						0x16: self.IFL,
						0x17: self.IFU,

						0x1a: self.ADX,
						0x1b: self.SBX,
						
						0x1e: self.STI,
						0x1f: self.STD
				}



		self.sopcodes = {  0x01 : self.JSR,

						   0x08 : self.INT,
						   0x09 : self.IAG,
						   0x0a : self.IAS,
						   0x0b : self.RFI,
						   
						   0x0c : self.IAQ,

						   0x10 : self.HWN,
						   0x11 : self.HWQ,

						   0x12 : self.HWI,
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
						0x18 : self.PPOP,
						0x19 : self.PEEK,
						0x1a : self.PICK,
						0x1b : self.SP,
						0x1c : self.PC,
						0x1d : self.EX,
						0x1e : self.ramPCpp,
						0x1f : self.PCpp

						#0x20-0x3f is treated as exception
					}


	def sopcode(self, o, a):
		print("SPECIALOP", hex(a))
		try:
			self.sopcodes[o](a)
		except (KeyError):
			if o >= 0x02 and o <=0x3f:
					print("RESERVED OPCODE:", hex(o))
			else:
					print("OPCODE DOESNT EXISTS:", hex(o))

	def PPOP(self, field):#TODO
		if field == 'a': #POP
			self.SP -= 0x0001
			return self.ram[self.SP]

		else: 			 #PUSH
			self.SP += 0x0001
			return self.ram[self.SP]


	def PEEK(self):
		return self.ram[self.SP]

	def PICK(self):
		return self.ram[ self.SP + self.PCpp() ]

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
		if isinstance(a, types.FunctionType):
			return a()
		else:
			return a

	def decode(self, i):
		# aaaaaabbbbbooooo
		opcode = i & 0x001f
		b = (i>>5) & 0x1f
		a = i>>10

		return (opcode, a, b)

	def ejec(self, i):
		(o, a, b) = self.decode(i)
		print( "OPCODE:", hex(o))
		self.opcodes[o](a, b)

	def dumpRam(self, i=None):
		print("\n ## RAM DUMP #######################################################")
		if i == None:
			length = len(self.ram)
		else: 
			length = i
		for i in range(0, length, 8):
			print( "{0:>8}: ".format(hex(i)), end="" )
			for j in range(0, 8):
				print( "{0:>6} ".format(hex(self.ram[i+j])), end="")
			print()
		print(" ###################################################################\n")

	def setRam(self, buf):
		for i in range(0, len(buf)):
			self.ram[i] = buf[i]
	
	def dumpReg(self):
		print("\n ## REGISTERS ######################################################")
		print("   A: {:>3}  B: {:>3}  C: {:>3}  X: {:>3} Y: {:>3} Z: {:>3} I: {:>3} J: {:>3}".format(\
				self.A, self.B, self.C, self.X, self.Y, self.Z, self.I, self.J))
		print("  PC: {:3} SP: {:3} EX: {:3} IA: {:3}".format(\
				self.PC, self.SP, self.EX, self.IA))
		print(" ###################################################################")

cpu = DCPU()
if len(sys.argv) > 1:
	ins = sys.argv[1:]
else:
	ins = [0x0411, 0x0412]
cpu.setRam([0x1111, 0x2222, 0x1234])
for i in ins:
	print ("Parameter: {}".format(i))
	cpu.ejec(int(str(i), 16))
cpu.dumpReg()
cpu.dumpRam(80)
	

