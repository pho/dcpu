import curses
from optparse import OptionParser
from time import sleep

import dcpu
from assembler import *
from devices import *


## Options Parsing
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
						  help="Assembly file", metavar="FILE")

parser.add_option("-s", "--step", action="store_true", dest="step",
						  help="Execution step-by-step")

parser.add_option("-l", "--slow", action="store_true", dest="slow",
						  help="Put a delay after every instruction")

parser.add_option("-d", "--debug", dest="debug", action="store_true",
						  help="Show every instruction executed", metavar="DEBUG")

(options, args) = parser.parse_args()

## Setup
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)
curses.start_color()


##
stdscr.border()
(scry, scrx) = stdscr.getbegyx()
(scrmaxy, scrmaxx) = stdscr.getmaxyx()

cbw = 76
cpuinfo = curses.newwin( scrmaxy-2 , cbw, scry + 3  , scrx + 1 )
(cby, cbx) = cpuinfo.getbegyx()

registers = cpuinfo.subwin(4, cbw-2, cby + 1 , cbx + 1)
registers.border()
registers.addstr(0, 3, "Registers")

ramy = (scrmaxy - 10) // 2
ram = cpuinfo.subwin(ramy, cbw -2, cby + 5, cbx + 1)
ram.border()
ram.addstr(0, 3, "RAM DUMP")

stack = cpuinfo.subwin(ramy, cbw -2, cby + 5 + ramy, cbx + 1)
stack.border()
stack.addstr(0, 3, "STACK DUMP")

monitor = curses.newwin(14, 34, cby + 1 , max( cbw+2, scrmaxx - 34 -2 ) )
monitor.border()


stdscr.addstr(1, 3, "DCPU-16 Emulator")
stdscr.addstr( scrmaxy - 2, 3, "r: run    s: step    q: quit")

###



def dumpReg(dcpu):
  registers.addstr(1, 1, "  A: {:>6}  B: {:>6}  C: {:>6}  X: {:>6}  Y: {:>6}  Z: {:>6} ".format(\
		  hex(dcpu.A()), hex(dcpu.B()), hex(dcpu.C()), hex(dcpu.X()), hex(dcpu.Y()), hex(dcpu.Z()) ))
  registers.addstr(2, 1,"  I: {:>6}  J: {:>6} PC: {:>6} SP: {:>6} EX: {:>6} IA: {:>6}".format(\
		  hex(dcpu.I()), hex(dcpu.J()), hex(dcpu.PC()), hex(dcpu.SP()), hex(dcpu.EX()), hex(dcpu.IA())))


def dumpRam(dcpu, i=None):
	if i == None:
		length = len(dcpu.ram)
	else: 
		length = i
	for i in range(0, length, 8):
		ret = ""
		ret += "{0:>8}: ".format(hex(i))
		for j in range(0, 8):
			ret += "{0:>6} ".format(hex(dcpu.ram[i+j]()))
		ram.addstr(i//8 + 1, 1, ret)

def dumpStack(dcpu, i=None):
	if i == None:
		r = dcpu.SP() % 8
		length = dcpu.SP() - r
	else: 
		length = 0xffff - i
	for i in range(length, 0xffff, 8):
		ret = ""
		ret += "{0:>8}: ".format(hex(i))
		for j in range(0, 8):
			ret += "{0:>6} ".format(hex(dcpu.ram[i+j]()))
		stack.addstr( (i-length)//8 +1, 1, ret)
		
def renderLEM(lem):
	## WONTFIX curses on python doesnt support all the color codes we need :(
	#for i in range(32):
	#	for j in range(12):
	#		(char, B, b, f) = lem.decodeColor(lem.ram[i+j]())

	monitor.addstr(7, 7, "Rendering not suppoted :(")



cpu = dcpu.DCPU()
lem = LEM1802()
cpu.attachDevice(lem)

if options.filename:
	#print("Loading", options.filename + "...", end="")
	stdscr.addstr(2, max( cbw+2, scrmaxx - 34 -2 ), "File loaded: {}".format(options.filename))
	f = assembly_file_plain(options.filename)
	code = list(map(lambda x: int(x, 16), f.split(" ")[:-1]))
	cpu.setRam(code)

else:
	if args:
		ins = list(map(lambda x: int(x, 16), args))
		print("STDIN:", ins)
	else:
		#ins = [0x0401, 0x0402]
		ins = []
	cpu.setRam(ins)

###########################################################


cpu.state = "STOPPED"
dumpReg(cpu)
dumpRam(cpu, 8*(ramy-2))
dumpStack(cpu, 8*(ramy-2))
stdscr.addstr(1, max( cbw+2, scrmaxx - 34 -2 ), "STATE: {}".format(cpu.state))

stdscr.refresh()
registers.refresh()
ram.refresh()
stack.refresh()
monitor.refresh()

while 1:

	if cpu.state != "STOPPED":
		if options.step:
			stdscr.nodelay(0)
		else:
			stdscr.nodelay(1)

		c = stdscr.getch()
		if c == ord('q'):
			break

		if options.slow:
			sleep(0.5)

		cpu.run()
		dumpReg(cpu)
		dumpRam(cpu, 8*(ramy-2))
		dumpStack(cpu, 8*(ramy-2))

	else:
		stdscr.nodelay(1)
		c = stdscr.getch()
		if c == ord('q'):
			break

		if c == ord('r'):
			cpu.PC(0x0)
			cpu.SP(0xffff)
			cpu.state = "PAUSED"

	stdscr.addstr(1, max( cbw+2, scrmaxx - 34 -2 ), "STATE: {}".format(cpu.state))

## Refresh all
	sleep(0.01)
	stdscr.refresh()
	registers.refresh()
	ram.refresh()
	stack.refresh()
	monitor.refresh()


## Clean up
curses.endwin()
