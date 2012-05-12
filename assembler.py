#!/usr/bin/python3
import sys, re
from optparse import OptionParser

opcodes = { "SET" : 0x01,
			"ADD" : 0x02,
			"SUB" : 0x03,
			"MUL" : 0x04,
			"MLI" : 0x05,
			"DIV" : 0x06,
			"DVI" : 0x07,
			"MOD" : 0x08,
			"MDI" : 0x09,
			"AND" : 0x0a,
			"BOR" : 0x0b,
			"XOR" : 0x0c,
			"SHR" : 0x0d,
			"ASR" : 0x0e,
			"SHL" : 0x0f,
			"IFB" : 0x10,
			"IFC" : 0x11,
			"IFE" : 0x12,
			"IFN" : 0x13,
			"IFG" : 0x14,
			"IFA" : 0x15,
			"IFL" : 0x16,
			"IFU" : 0x17,

			"ADX" : 0x1a,
			"SBX" : 0x1b,

			"STI" : 0x1e,
			"STD" : 0x1f,
			}


##			SOPCODES

sopcodes= {	"JSR" : 0x0100000,

			"INT" : 0x0800000,
			"IAG" : 0x0900000,
			"IAS" : 0x0a00000,
			"RFI" : 0x0b00000,
			"IAQ" : 0x0c00000,

			"HWN" : 0x1000000,
			"HWQ" : 0x1100000,
			"HWI" : 0x1200000,

			}

values = { "A"  : 0x00,
		   "B"  : 0x01,
		   "C"  : 0x02,
		   "X"  : 0x03,
		   "Y"  : 0x04,
		   "Z"  : 0x05,
		   "I"  : 0x06,
		   "J"  : 0x07,
		   "[A]"  : 0x08,
		   "[B]"  : 0x09,
		   "[C]"  : 0x0a,
		   "[X]"  : 0x0b,
		   "[Y]"  : 0x0c,
		   "[Z]"  : 0x0d,
		   "[I]"  : 0x0e,
		   "[J]"  : 0x0f,
		   #TODO
		   "PPOP" : 0x18,
		   "[SP]" : 0x19,
		   "PICK" : 0x1a,
		   "SP" : 0x1b,
		   "PC" : 0x1c,
		   "EX" : 0x1d,
		   "NEXTWL" : 0x1e,
		   "NEXTW" : 0x1f,
		   }


def assembly(buf):
	ap1=None
	ap2=None
	i = buf.split()

	if i[0] in opcodes.keys():
		o = opcodes[i[0]]
		#print("OPCODE:", hex(o))
		
		#Get b
		try:
			b = values[i[1]]
		#	print("b:", hex(b))
		except:
			r = re.match("^\[(0x..?.?.?)\]$", i[1])
			if r:
				b = values["NEXTW"]
				ap1 = r.group(1)
			else:
				r = re.match("^(0x..?.?.?)$", i[1])
				if r:
					b = values["NEXTWL"]
					ap1 = r.group(1)
				else:
					print("WRONG INSTRUCTION:", buf)
					sys.exit(-1)


		# Get a
		try:
			a = values[i[2]]
			#print("a:", hex(a))
		except:
			r = re.match("^\[(0x..?.?.?)\]$", i[2])
			if r:
				a = values["NEXTW"]
				ap2 = r.group(1)

			else:
				r = re.match("^(0x..?.?.?)$", i[2])
				if r:
					a = values["NEXTWL"]
					ap2 = r.group(1)
				else:
					print("WRONG INSTRUCTION:", buf)
					sys.exit(-1)
		
		ret = "{} ".format(hex((((a<<5) + b)<<5) + o) )

		if ap1:
			ret += "{} ".format(hex(int(ap1, 16)))

		if ap2:
			ret += "{} ".format(hex(int(ap2, 16)))

		return ret

if len(sys.argv) > 1:
	ins = " ".join(sys.argv[1:])
else:
	ins = "SET A PC"


def assembly_file(filename):
	f = open(filename, 'r')
	print("######################")
	print("## DCPU16 ASM Code: ##")
	print("######################")
	print()

	for line in f:
		if line.split()[0] != ';':
			asm = assembly(line[:-1])
			if asm:
				print(asm, end=" ")
			else:
				print("#", line[:-1], "#")
				print("#", line.split(), "#")
				print("WARNING HERE")

	print()
	print()
	print("######################")






######################

#print(ins)
#print(assembly(ins))

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
		                  help="Assembly file", metavar="FILE")

(options, args) = parser.parse_args()

if options.filename:
	f = assembly_file(options.filename)
