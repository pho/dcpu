#!/usr/bin/python3.2
import sys, types
import weakref

class Cell(int):
	def __init__(self, i=0x0000):
		self.value = i
	def __call__(self, arg=None):
		if arg == None:
			return self.value
		else:
			print(self.value, "-->", arg)
			self.value = arg

ram = [0x0000] * 65535
A, B, C, X, Y, Z, I, J = \
	0x0002,0x0008,0x0000,0x0000,0x0000,0x0000,0x0000,0x0000

PC, SP, EX, IA = \
	0x1234,0x0001,0x0000, 0x0000

class DCPU:

	def __init__(self):
		global A,B,C,X,Y,Z,I,J,PC,SP,EX,IA,ram
	#	self.A, self.B, self.C, self.X, self.Y, self.Z, self.I, self.J = \
	#		Cell(0x0002),Cell(0x0008),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000)

	#	self.PC, self.SP, self.EX, self.IA = \
	#		Cell(0x1234),Cell(0x0001),Cell(0x0000), Cell(0x0000)
		
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
						0x00 : A,
						0x01 : B,
						0x02 : C,
						0x03 : X,
						0x04 : Y,
						0x05 : Z,
						0x06 : I,
						0x07 : J,
						0x08 : ram[A],
						0x09 : ram[B],
						0x0a : ram[C],
						0x0b : ram[X],
						0x0c : ram[Y],
						0x0c : ram[Z],
						0x0e : ram[I],
						0x0f : ram[J],
						#TODO
						0x18 : self.PPOP,
						0x19 : self.PEEK,
						0x1a : self.PICK,
						0x1b : SP,
						0x1c : PC,
						0x1d : EX,
						0x1e : self.ramPCpp,
						0x1f : self.PCpp

						#0x20-0x3f is treated as exception
					}

	def SET(self, a, b):
		global A,B,C,X,Y,Z,I,J,PC,SP,EX,IA,ram
		A += 0x1
		print("SET", hex(a), hex(b))
		v1 = self.resolve(a, 'a')
		v2 = self.resolve(b, 'b')
		v1=v2
		self.PCpp()
		ram[10] = 0xffff

	def ADD(self, a, b):
		global A,B,C,X,Y,Z,I,J,PC,SP,EX,IA,ram
		print("ADD", hex(a), hex(b))
		if a == 0xffff:
			EX = 0x0001
		else:
			EX = 0x0000
		#ram[a]( (ram[a]() + b) % 0xffff )

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

	def sopcode(self, o, a):
		print("SPECIALOP", hex(a))
		try:
			self.sopcodes[o](a)
		except (KeyError):
			if o >= 0x02 and o <=0x3f:
					print("RESERVED OPCODE:", hex(o))
			else:
					print("OPCODE DOESNT EXISTS:", hex(o))

	def PPOP(self, field):
		global ram, SP
		if field == 'a': #POP
			SP -= 0x0001
			return ram[SP]

		else: 			 #PUSH
			SP += 0x0001
			return ram[SP]


	def PEEK(self):
		global ram, SP
		return ram[SP]

	def PICK(self): 
		global ram, SP
		return ram[ SP + self.PCpp() ]

	def PCpp(self):
		global PC,SP
		PC += 0x0001
		print("PC++:", PC)
		return PC
		
	def ramSP(self):
		global SP, ram
		return ram[SP]

	def ramPCpp(self):
		global PC, ram
		self.PCpp()
		return ram[PC]


####
	def resolve(self, a, args=None): #TODO Check this..
		if a in self.values.keys():
			if isinstance(self.values[a], types.FunctionType):
				if args == None:
					return self.values[a]()
				else:
					return self.values[a](args)
			else:
				r = weakref.ref(self.values[a])
				print(r)
				return r
		else:
			print("\n\nINVALID PARAMETER")
			print("You are on your own...\n\n")


	def decode(self, i):
		# aaaaaabbbbbooooo
		opcode = i & 0x001f
		print("opcode:", hex(opcode))
		print("i>>5:", hex(i>>5))
		print("i>>10:", hex(i>>10))
		b = (i>>5) & 0x1f
		a = i>>10

		return (opcode, a, b)

	def ejec(self, i):
		(o, a, b) = self.decode(i)
		print( "OPCODE: ", hex(o))
		self.opcodes[o](a, b)

	def dumpRam(self, i=None):
		print("\n ## RAM DUMP #######################################################")
		if i == None:
			length = len(ram)
		else: 
			length = i
		for i in range(0, length, 8):
			print( "{0:>8}: ".format(hex(i)), end="" )
			for j in range(0, 8):
				print( "{0:>6} ".format(hex(ram[i+j])), end="")
			print()
		print(" ###################################################################\n")

	def setRam(self, buf):
		for i in range(0, len(buf)):
			ram[i] = buf[i]
	
	def dumpReg(self):
		print("\n ## REGISTERS ######################################################")
		print("  A: {:>6}  B: {:>6}  C: {:>6}  X: {:>6}  Y: {:>6}  Z: {:>6} ".format(\
				hex(A), hex(B), hex(C), hex(X), hex(Y), hex(Z), ))
		print("  I: {:>6}  J: {:>6} PC: {:>6} SP: {:>6} EX: {:>6} IA: {:>6}".format(\
				hex(I), hex(J), hex(PC), hex(SP), hex(EX), hex(IA)))
		print(" ###################################################################")

cpu = DCPU()

if len(sys.argv) > 1:
	ins = " ".join(sys.argv[1:]).split()
else:
	ins = [0x0411, 0x0412]

cpu.setRam([0x1111, 0x2222, 0x1234])
for i in ins:
	print ("Parameter: {}".format(hex(int(str(i), 16))))
	cpu.ejec(int(str(i), 16))

cpu.dumpReg()
cpu.dumpRam(80)
	

