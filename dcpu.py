#!/usr/bin/python3.2
import sys, types
import weakref

#class Cell(int):
#	def __init__(self, i=0x0000):
#		self.value = i
#	def __call__(self, arg=None):
#		if arg == None:
#			return self.value
#		else:
#			print(self.value, "-->", arg)
#			self.value = arg
#	def __repr__(self):
#		return "Im a Cell: {} {}".format(self, self.value)
#
class Cell(int):
	def __init__(self, a=0x0):
		self.v = a

	def __call__(self, a = None):
		if a == None:
			return self.v
		else:
			self.v = a 
	def __repr__(self):
		return str(self.v)


class Getter(int):
	def __init__(self, v):
		self.value = v
	def __call__(self, arg=None):
		return self.value

#class PCinc(object):
#	def __init__(self, f):
#		global PC
#		f()
#		PC += 0x0001
#	def __call__(self):
#		f()
#	
#class incPC(object):
#	def __init__(self, f):
#		global PC
#		PC += 0x0001
#		f()
#	def __call__(self):
#		f()
#

def incPC(f):
	def wrap(self):
		print("AMA decorator")
		global PC
		self.PCpp()
		return f(self)
	return wrap

def PCinc(f):
	def wrap(self):
		global PC
		f(self)
		self.PCpp()
		
	print("AMA decorator")
	return wrap

ram = []
for i in range(0, 0x10000):
	ram.append(Cell())

A, B, C, X, Y, Z, I, J = \
	Cell(0x0002),Cell(0x0008),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000)

PC, SP, EX, IA = \
	Cell(0x0000),Cell(0x0000),Cell(0x0000), Cell(0x0000)

class DCPU:

	def __init__(self):
		
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
						0x08 : self.ram_A,
						0x09 : self.ram_B,
						0x0a : self.ram_C,
						0x0b : self.ram_X,
						0x0c : self.ram_Y,
						0x0c : self.ram_Z,
						0x0e : self.ram_I,
						0x0f : self.ram_J,
						#TODO
						0x18 : self.PPOP,
						0x19 : self.PEEK,
						0x1a : self.PICK,
						0x1b : self.SP,
						0x1c : self.PC,
						0x1d : self.EX,
						0x1e : self.NW, #self.ramPCpp,
						0x1f : self.ramNW #PCpp

						#0x20-0x3f is treated as exception
					}

	def SET(self, b, a):
		print("SET", hex(b), hex(a))

		v1 = self.resolve(b, 'a')
		v2 = self.resolve(a, 'b')
		
		v1(v2())

	def ADD(self, b, a):
		global ram
		print("ADD", hex(b), hex(a))

		v1 = self.resolve(a, 'a')
		v2 = self.resolve(b, 'b')

		print(type(v1), type(v2))
		print("vals:", v1(), v2())

		if v2() + v1() > 0xffff:
			EX = 0x0001
		else:
			EX = 0x0000
		
		v1((v2() + v1()) % 0xffff)

	def SUB(self, a, b):
		global ram
		print("SUB", hex(b), hex(a))

		v1 = self.resolve(a, 'a')
		v2 = self.resolve(b, 'b')

		if v2() - v1() < 0x0000:
			EX = 0xffff
		else:
			EX = 0x0000
		
		v1(v2() - v1() % 0xffff)
	
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

	## VALUES

	def A(self, a=None):
		global A
		return A
		if a == None:
			return A
		else:
			print("A is now:", a)
			A = a

	def B(self, b=None):
		global B
		return B
		if b == None:
			return B
		else:
			B = b

	def C(self, c=None):
		global C
		return C
		if c == None:
			return C
		else:
			C = c

	def X(self, c=None):
		global X
		return X
		if c == None:
			return X
		else:
			X = c

	def Y(self, c=None):
		global Y
		return Y
		if c == None:
			return Y
		else:
			Y = c

	def Z(self, c=None):
		global Z
		return Z
		if c == None:
			return Z
		else:
			Z = c

	def I(self, c=None):
		global I
		return I
		if c == None:
			return I
		else:
			I = c

	def J(self, c=None):
		global J
		return J

		if c == None:
			return J
		else:
			J = c

	def PC(self, c=None):
		global PC
		return PC
		if c == None:
			return PC
		else:
			PC = c

	def SP(self, c=None):
		global SP
		return SP
		if c == None:
			return SP
		else:
			SP = c

	def EX(self, c=None):
		global EX
		return EX
		if c == None:
			return EX
		else:
			EX = c

	def IA(self, c=None):
		global IA
		return IA
		if c == None:
			return IA
		else:
			IA = c

	def ram_A(self, c=None):
		global ram
		return ram[A]
		if c == None:
			return ram[A]
		else:
			ram[A] = c

	def ram_B(self, c=None):
		global ram
		return ram[B]
		if c == None:
			return ram[B]
		else:
			ram[B] = c

	def ram_C(self, c=None):
		global ram
		return ram[C]
		if c == None:
			return ram[C]
		else:
			ram[C] = c

	def ram_X(self, c=None):
		global ram
		return ram[X]
		if c == None:
			return ram[X]
		else:
			ram[X] = c

	def ram_Y(self, c=None):
		global ram
		return ram[Y]
		if c == None:
			return ram[Y]
		else:
			ram[Y] = c

	def ram_Z(self, c=None):
		global ram
		return ram[Z]
		if c == None:
			return ram[Z]
		else:
			ram[Z] = c

	def ram_I(self, c=None):
		global ram
		return ram[I]
		if c == None:
			return ram[I]
		else:
			ram[I] = c

	def ram_J(self, c=None):
		global ram
		return ram[J]
		if c == None:
			return ram[J]
		else:
			ram[J] = c

	def PPOP(self, field):
		global ram
		if field == 'a': #POP
			self.SP( self.SP() - 0x0001 )
			return ram[self.SP()]

		else: 			 #PUSH
			self.SP( self.SP() + 0x0001 )
			return ram[self.SP()]


	def PEEK(self, c=None):
		global ram
		return ram[self.SP()]

	def PICK(self, c=None): 
		global ram
		return ram[ self.SP() + self.PCpp() ]

	def PCpp(self, c=None):
		global PC
		PC( PC() + 0x0001 )
		return PC()
		
	def ramSP(self, c=None):
		global ram
		return ram[self.SP()]

	def NW(self, field=None):
		global ram, PC
		self.PCpp()
		print("nextword:", hex(ram[PC()]()))
		return ram[PC()]
		return ram[self.PC()]

	def ramNW(self, field=None):
		global ram
		self.PCpp()
		print("[nextword]:", hex(ram[ram[self.PC()]]))
		print(type(ram[ram[self.PC()]]))
		return ram[ram[self.PC()]]


####
	def resolve(self, a, args=None): #TODO Check this..
		if a in self.values.keys():
			if isinstance(self.values[a], types.MethodType):
				if args == None:
					return self.values[a]()
				else:
					return self.values[a](args)
			else:
				#r = weakref.ref(self.values[a])
				#print(r)
				return self.values[a]
		else:
			print("\n\nINVALID PARAMETER")
			print("You are on your own...\n\n")


	def decode(self, i):
		# aaaaaabbbbbooooo
		opcode = i & 0x001f
		#print("opcode:", hex(opcode))
		#print("i>>5:", hex(i>>5))
		#print("i>>10:", hex(i>>10))
		b = (i>>5) & 0x1f
		a = i>>10

		return (opcode, a, b)

	def ejec(self, i):
		(o, a, b) = self.decode(i)
		print( "OPCODE: ", hex(o))
		self.opcodes[o](b, a)

	def dumpRam(self, i=None):
		print("\n ## RAM DUMP #######################################################")
		if i == None:
			length = len(ram)
		else: 
			length = i
		for i in range(0, length, 8):
			print( "{0:>8}: ".format(hex(i)), end="" )
			for j in range(0, 8):
				print( "{0:>6} ".format(hex(ram[i+j]())), end="")
			print()
		print(" ###################################################################\n")

	def setRam(self, buf):
		global ram
		for i in range(0, len(buf)):
			ram[i](buf[i])
	
	def dumpReg(self):
		print("\n ## REGISTERS ######################################################")
		print("  A: {:>6}  B: {:>6}  C: {:>6}  X: {:>6}  Y: {:>6}  Z: {:>6} ".format(\
				hex(A()), hex(B()), hex(C()), hex(X()), hex(Y()), hex(Z()), ))
		print("  I: {:>6}  J: {:>6} PC: {:>6} SP: {:>6} EX: {:>6} IA: {:>6}".format(\
				hex(I()), hex(J()), hex(PC()), hex(SP()), hex(EX()), hex(IA())))
		print(" ###################################################################")

cpu = DCPU()

if len(sys.argv) > 1:
	ins = " ".join(sys.argv[1:]).split()
	cpu.setRam(sys.argv[1:])
else:
	ins = [0x0411, 0x0412]

cpu.setRam([0x7801, 0xffff, 0x7021, 0x7002])
#for i in ins:
	#print ("Parameter: {}".format(hex(int(str(i), 16))))
	#cpu.ejec(int(str(i), 16))

i = ram[PC()]()
while i != 0x0000:
#or k in range(0, 3):

	print("ins:", hex(ram[PC()]())) 
	cpu.ejec(ram[PC()]())
	cpu.PCpp()
	i = ram[PC()]()
	print("\n>>\n")

cpu.dumpReg()
cpu.dumpRam(80)
	

