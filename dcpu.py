#!/usr/bin/python
import sys, types
from optparse import OptionParser
from collections import deque

from assembler import *
from devices import *


class Cell(int):
	def __init__(self, a=0x0):
		self.v = a

	def __call__(self, a = None):
		if a == None:
			return self.v
		else:
			self.v = (a % 0x10000) 
	def __repr__(self):
		return str(self.v)



class DCPU:

	def __init__(self):
		self.ram = []
		for i in range(0, 0x10000):
			self.ram.append(Cell())

		self.A, self.B, self.C, self.X, self.Y, self.Z, self.I, self.J = \
			Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000),\
			Cell(0x0000),Cell(0x0000),Cell(0x0000),Cell(0x0000)

		self.PC, self.SP, self.EX, self.IA = \
			Cell(0x0000),Cell(0xffff),Cell(0x0000), Cell(0x0000)
		
		self.opcodes = {
				0x0 : self.sopcode,
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



		self.sopcodes = {
				0x01 : self.JSR,

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
				0x10 : self.A_NW,
				0x11 : self.B_NW,
				0x12 : self.C_NW,
				0x13 : self.X_NW,
				0x14 : self.Y_NW,
				0x15 : self.Z_NW,
				0x16 : self.I_NW,
				0x17 : self.J_NW,
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

		self.intqEnabled = False
		self.intQueue = deque()
		self.devices = []
		self.state = "PAUSED"

	def SET(self, b, a):
		#print("SET", hex(b), hex(a))

		v1 = self.resolve(b, 'a')
		v2 = self.resolve(a, 'b')
		
		v1(v2())

	def ADD(self, a, b):
		#print("ADD", hex(a), hex(b))

		v1 = self.resolve(a, 'a')
		v2 = self.resolve(b, 'b')

		if v2() + v1() > 0xffff:
			print("Overflow")
			self.EX(0x0001)
		else:
			self.EX(0x0000)
		
		v3 = v1() + v2()
		v3 = v3 % 0xffff
		#print("ADD:", v3 )
		v1(v3)

	def SUB(self, a, b):
		#print("SUB", hex(a), hex(b))

		v1 = self.resolve(a, 'a')
		v2 = self.resolve(b, 'b')

		if v2() > v1():
			print("Underflow")
			self.EX(0xffff)
		else:
			self.EX(0x0000)
		
		v3 = v1() - v2()
		v3 = v3 % 0xffff
		#print("SUB:", hex(v3) )
		v1(v3)
	
	def MUL(self, b, a):
		#print("MUL", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		self.EX(((argB()*argA())>>16)&0xffff)

		argB( argA() * argB() )

	def MLI(self, a, b):
		print("MLI not implemented")

	def DIV(self, b, a):
		#print("DIV", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')


		if argA() == 0:
			self.EX(0x0)
			argB(0x0)
		else:
			self.EX(((argB()<<16)/argA())&0xffff )
			argB( argB()/ argA() )
		
	def DVI(self, a, b):
		#TODO
		print("DVI not implemented")

	def MOD(self, b, a):
		#print("MOD", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		if argA() == 0:
			argB(0x0)
		else:
			argB( argB() % argA() )

	def MDI(self, a, b):
		#TODO
		print("MDI not implemented")

	def AND(self, b, a):
		#print("AND", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		argB( argB() & argA() )

	def BOR(self, b, a):
		#print("BOR", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		argB( argB() | argA() )

	def XOR(self, b, a):
		#print("XOR", hex(b), hex(a))
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		argB( argB() ^ argA() )

	def SHL(self, b, a):
		# http://stackoverflow.com/a/5833119
		#print("SHL")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		EX(( (argB() << argA() ) >> 16 ) & 0xffff)
		argB( argB() << argA() )

	def SHR(self, b, a):
		#print("SHR")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		EX(( (argB() << 16 ) >> argA() ) & 0xffff)
		argB( (argB() % 0x100000000) >> argA() )

	def IFE(self, b, a):
		#print("IFE")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		if not argB() == argA():
			self.PCpp()
			self.skipLiteral()

	def IFL(self, b, a):
		#print("IFL")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		if not argB() > argA():
			self.PCpp()
			self.skipLiteral()

	def IFA(self, b, a):
		#print("IFA")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		#TODO Signed
		if not argB() > argA():
			self.PCpp()
			self.skipLiteral()

	def IFN(self, b, a):
		#print("IFN")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		if argB() == argA():
			self.PCpp()
			self.skipLiteral()

	def IFU(self, b, a):
		#print("IFU" )
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		#TODO Signed
		if not argB() < argA():
			self.PCpp()
			self.skipLiteral()

	def IFG(self, b, a):
		#print("IFG")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		#TODO Signed
		if  argB() <= argA():
			self.PCpp()
			self.skipLiteral()

	def IFB(self, b, a):
		#print("IFB")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		#TODO Signed
		if not ( argB() & argA() ) != 0:
			self.PCpp()
			self.skipLiteral()

	def ADX(self, b, a):
		#print("ADX")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		res = argB() + argA() + EX()
		if res > 0xffff:
			EX(0x1)
		else:
			EX(0x0)
		argB(res)

	def ASR(self, b, a):
		#print("ASR")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		EX(( ( (argB() << 16 ) % 0x100000000) >> argA() ) & 0xffff)
		argB( argB() >> argA() )

	def IFC(self, b, a):
		#print("IFC")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		#TODO Signed
		if not ( argB() & argA() ) == 0:
			self.PCpp()
			self.skipLiteral()

	def SBX(self, b, a):
		#print("SBX")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')
		res = argB() - argA() + EX()
		if res < 0x0000:
			EX(0xffff)
		else:
			EX(0x0)
		argB(res)

	
	def STI(self, b, a):
		#print("STI")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		argB( argA() )
		I( I() + 1 )
		J( J() + 1 )

	def STD(self, b, a):
		#print("STD")
		argB = self.resolve(b, '1')
		argA = self.resolve(a, '2')

		argB( argA() )
		I( I() - 1 )
		J( J() - 1 )

## SOPCODES

	def INT(self, a):
		argA = self.resolve(a, '1')
		if self.IA() != 0:
			if self.intqEnabled == True:
				self.intQueue.append(a)

			else:
				self.intqEnabled = True

				self.ram[self.SP()] = self.PC()
				self.SP( (self.SP() - 0x0001 ) % 0x10000 )

				self.ram[self.SP()] = self.A()
				self.SP( (self.SP() - 0x0001 ) % 0x10000 )

				self.PC(self.IA())
				self.A(argA())

	def IAG(self, a):
		argA = self.resolve(a, '1')
		argA( self.IA() )

	def IAS(self, a):
		argA = self.resolve(a, '1')
		self.IA( argA() )

	def RFI(self, a):
		v = self.ram[self.SP()]
		self.SP( (self.SP() + 0x0001 ) % 0x10000 )
		
		self.A( v() )

		v = self.ram[self.SP()]
		self.SP( (self.SP() + 0x0001 ) % 0x10000 )

		self.PC( v() )

		self.intqEnabled = False

	def IAQ(self, a):
		argA = self.resolve(a, '1')
		if argA() == 0:
			self.intqEnabled = False
		else:
			self.intqEnabled = True

	def HWN(self, a):
		argA = self.resolve(a, '1')
		argA( len(self.devices) )

	def HWQ(self, a):
		argA = self.resolve(a, '1')
		(A, B, C, X, Y) = self.devices[argA()].get_info()
		self.A(A)
		self.B(B)
		self.C(C)
		self.X(X)
		self.Y(Y)

	def HWI(self, a):
		argA = self.resolve(a, '1')
		self.devices[argA()].hwi(self)

	def JSR(self, a):
		self.ram[self.SP()] = self.PC() + 1
		self.SP( (self.SP() - 0x0001 ) % 0x10000 )
		self.PC(a)

	def sopcode(self, o, a):
		#print("SPECIALOP", hex(a))
		try:
			argA = self.resolve(a, '1')
			
			self.sopcodes[o](argA)
		except (KeyError):
			if o >= 0x02 and o <=0x3f:
					print("RESERVED OPCODE:", hex(o))
			else:
					print("OPCODE DOESNT EXISTS:", hex(o))

	## VALUES

	def ram_A(self, c=None):
		return self.ram[self.A()]

	def ram_B(self, c=None):
		return self.ram[self.B()]

	def ram_C(self, c=None):
		return self.ram[self.C()]

	def ram_X(self, c=None):
		return self.ram[self.X()]

	def ram_Y(self, c=None):
		return self.ram[self.Y()]

	def ram_Z(self, c=None):
		return self.ram[self.Z()]

	def ram_I(self, c=None):
		return self.ram[self.I()]

	def ram_J(self, c=None):
		return self.ram[self.J()]

	def A_NW(self, c=None):
		return self.ram[A() + self.NW()]

	def B_NW(self, c=None):
		return self.ram[B() + self.NW()]

	def C_NW(self, c=None):
		return self.ram[C() + self.NW()]

	def X_NW(self, c=None):
		return self.ram[X() + self.NW()]

	def Y_NW(self, c=None):
		return self.ram[Y() + self.NW()]

	def Z_NW(self, c=None):
		return self.ram[Z() + self.NW()]

	def I_NW(self, c=None):
		return self.ram[I() + self.NW()]

	def J_NW(self, c=None):
		return self.ram[J() + self.NW()]

	def PPOP(self, field):
		if field == 'b': #POP
			v = self.ram[self.SP()]
			#Stack can overwrite code
			#if self.SP() > (self.SP() + 0x0001) % 0x10000:
			#	return v

			self.SP( (self.SP() + 0x0001 ) % 0x10000 )
			return v

		else: 			 #PUSH
			self.SP( (self.SP() - 0x0001 ) % 0x10000 )
			return self.ram[self.SP()]


	def PEEK(self, c=None):
		return self.ram[self.SP()]

	def PICK(self, c=None): 
		return self.ram[ self.SP() + self.NW() ]

	def PCpp(self, c=None):
		self.PC( self.PC() + 0x0001 )
		return self.PC()
	
	def skipLiteral(self):
		#if next instr. has a literal, skip ip too
		(no, na, nb) = self.decode(self.ram[self.PC()]())
		if na == 0x1f or nb == 0x1f or na == 0x1e or nb == 0x1e:
			self.PCpp()

	def attachDevice(self, device):
		self.devices.append(device)

	#unused?
	def ramSP(self, c=None):
		return self.ram[self.SP()]

	def NW(self, field=None):
		self.PCpp()
		#print("nextword:", hex(self.ram[self.PC()]()))
		return self.ram[self.PC()]

	def ramNW(self, field=None):
		self.PCpp()
		#print("[nextword]:", hex(self.ram[self.ram[self.PC()]]))
		return self.ram[self.ram[self.PC()]]


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
		#print( "OPCODE: ", hex(o))
		self.opcodes[o](b, a)

	def dumpRam(self, i=None):
		print("\n ## RAM DUMP #######################################################")
		if i == None:
			length = len(self.ram)
		else: 
			length = i
		for i in range(0, length, 8):
			print( "{0:>8}: ".format(hex(i)), end="" )
			for j in range(0, 8):
				print( "{0:>6} ".format(hex(self.ram[i+j]())), end="")
			print()
		print(" ###################################################################\n")

	def dumpStack(self, i=None):
		print("\n ## STACK DUMP #####################################################")
		if i == None:
			r = self.SP() % 8
			length = self.SP() - r
		else: 
			length = 0xffff - i
		for i in range(length, 0xffff, 8):
			print( "{0:>8}: ".format(hex(i)), end="" )
			for j in range(0, 8):
				print( "{0:>6} ".format(hex(self.ram[i+j]())), end="")
			print()
		print(" ###################################################################\n")

	def setRam(self, buf):
		for i in range(0, len(buf)):
			self.ram[i](buf[i])
	
	def dumpReg(self):
		print(" ## REGISTERS ######################################################")
		print("  A: {:>6}  B: {:>6}  C: {:>6}  X: {:>6}  Y: {:>6}  Z: {:>6} ".format(\
				hex(self.A()), hex(self.B()), hex(self.C()), hex(self.X()), hex(self.Y()), hex(self.Z()) ))
		print("  I: {:>6}  J: {:>6} PC: {:>6} SP: {:>6} EX: {:>6} IA: {:>6}".format(\
				hex(self.I()), hex(self.J()), hex(self.PC()), hex(self.SP()), hex(self.EX()), hex(self.IA())))
		print(" ###################################################################")


	def checkInt(self):
		if self.IA() != 0 and len(self.intQueue) > 0 and self.intqEnabled == False:
			intcode = self.intQueue.popleft()
			self.INT(self, intcode)
	
	def run(self):
		i = self.ram[self.PC()]()

		if i != 0x0000:
			self.checkInt()
			self.ejec(self.ram[self.PC()]())
			self.PCpp()
			self.state = "RUNNING"
		else:
			self.state = "STOPPED"

if __name__ == "__main__":
	cpu = DCPU()
	monitor = LEM1802()
	monitor.render()
	cpu.attachDevice(monitor)

######################

	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
							  help="Assembly file", metavar="FILE")

	parser.add_option("-s", "--step", action="store_true", dest="step",
							  help="Execution step-by-step")

	parser.add_option("-d", "--debug", dest="debug", action="store_true",
							  help="Show every instruction executed", metavar="DEBUG")

	(options, args) = parser.parse_args()

	if options.filename:
		print("Loading", options.filename + "...", end="")
		f = assembly_file_plain(options.filename)
		code = list(map(lambda x: int(x, 16), f.split(" ")[:-1]))
		cpu.setRam(code)
		print(" done\n")
	else:
		if args:
			ins = list(map(lambda x: int(x, 16), args))
			print("STDIN:", ins)
		else:
			#ins = [0x0401, 0x0402]
			ins = []
		cpu.setRam(ins)



	i = cpu.ram[cpu.PC()]()
	c = 0
	while cpu.state != "STOPPED":
		if options.debug or options.step:
			print(" ## Cycle", c, ":", hex(cpu.ram[cpu.PC()]())) 

			cpu.dumpReg()
			cpu.dumpRam(80)
			cpu.dumpStack()

		if options.step:
			input()

		cpu.run()
		
		c+=1

	if options.debug:
		print(" ## END ##")

	cpu.dumpReg()
	cpu.dumpRam(80)
	cpu.dumpStack()

