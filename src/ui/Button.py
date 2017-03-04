#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
from ProgramException import *

# Button class for Curses.
class Button:
	parent = None
	label = ""
	callback = None
	callbackArgs = None
	callbackKWArgs = None
	win = None
	
	def __init__(self, parent, label, sizeYX=None, positionYX=(0,0)):
		self.parent = parent
		self.label = label
		if sizeYX is None:
			sizeYX = (1, 5 + len(label))
		self.win = parent.derwin(
			sizeYX[0],
			sizeYX[1],
			positionYX[0],
			positionYX[1]
		)
	
	def setCallback(self, callback, *args, **kwargs):
		self.callback = callback
		self.callbackArgs = args
		self.callbackKWArgs = kwargs
	
	def onFocus(self):
		self.win.addstr(0, 0, "> " + self.label + " <", curses.A_REVERSE)
		self.redraw()
	
	def onLoseFocus(self):
		self.win.addstr(0, 0, "< " + self.label + " >", curses.A_NORMAL)
		self.redraw()
	
	def redraw(self):
		self.win.refresh()
	
	def onInput(self, inputChar):
		if inputChar == ord('\n') or inputChar == curses.KEY_ENTER or inputChar == ord(' '):
			if self.callback == None:
				raise MissingCallback()
			else:
				return self.callback(*self.callbackArgs, **self.callbackKWArgs)
		return None