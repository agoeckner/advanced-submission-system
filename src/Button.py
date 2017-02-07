#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses

# Button class for Curses.
class Button:
	parent = None
	label = ""
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
	
	def onFocus(self):
		self.win.addstr(0, 0, "> " + self.label + " <", curses.A_REVERSE)
		self.redraw()
	
	def onLoseFocus(self):
		self.win.addstr(0, 0, "< " + self.label + " >", curses.A_NORMAL)
		self.redraw()
	
	def redraw(self):
		self.win.refresh()
	
	def onInput(self, inputChar):
		if inputChar == curses.KEY_ENTER:
			pass
		return None