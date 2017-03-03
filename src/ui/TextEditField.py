#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import curses.textpad
from ProgramException import *

# TextEditField class for Curses.
class TextEditField:
	def __init__(self, parent, maxLength=0, defaultValue="", sizeYX=(1,15), positionYX=(0,0)):
		self.callback = None
		self.parent = parent
		self.defaultValue = defaultValue
		self.textStyle = curses.A_NORMAL
		if sizeYX[0] < 1 or sizeYX[1] < 3:
			raise ComponentSizeInvalid("TextEditField must have minimum size (1, 3)")
		if maxLength > 0 and maxLength + 3 > sizeYX[1]:
			raise ComponentSizeInvalid("TextEditField size X must be 3 greater "
				"than maximum text length.")
		elif maxLength <= 0:
			self.maxLength = sizeYX[1] - 3;
		else:
			self.maxLength = maxLength
		self.sizeYX = sizeYX
		self.win = parent.derwin(
			sizeYX[0],
			sizeYX[1],
			positionYX[0],
			positionYX[1]
		)
		self.textArea = self.win.derwin(
			sizeYX[0],
			sizeYX[1] - 2,
			0,
			1
		)
		self.textBox = TextBox(self.textArea)
		self.textBox.do_command(curses.ascii.VT) #clear the stupid thing
	
	def setCallback(self, callback, *args, **kwargs):
		self.callback = callback
		self.callbackArgs = args
		self.callbackKWArgs = kwargs
	
	def getValue(self):
		return self.textBox.gather()
	
	def getMaxLength(self):
		return self.maxLength
	
	def onFocus(self):
		self.textStyle = curses.A_REVERSE
		self.redraw()
	
	def onLoseFocus(self):
		self.textStyle = curses.A_NORMAL
		self.redraw()
	
	def redraw(self):
		self.win.addch(0, 0, "[", self.textStyle)
		# Work around a bug with curses.
		# http://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses
		try:
			self.win.addch(0, self.sizeYX[1] - 1, "]", self.textStyle)
		except curses.error:
			pass
		self.win.refresh()
	
	def onInput(self, inputChar):
		if inputChar == ord('\n') or inputChar == curses.KEY_ENTER:
			if self.callback == None:
				raise MissingCallback()
			else:
				return self.callback(*self.callbackArgs, **self.callbackKWArgs)
		else:
			self.textBox.do_command(inputChar)
		return None

class TextBox(curses.textpad.Textbox):
	pass