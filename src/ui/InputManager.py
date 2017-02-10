#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses

# InputManager handles tabbing between elements in a UI, determining which receives user input.
class InputManager:
	parent = None
	elements = []
	currentIdx = 0
	currentElement = None
	def __init__(self, parent):
		self.parent = parent
		self.elements = []
		self.currentIdx = 0
		self.currentElement = None
	
	# Adds a UI element to the manager.
	def addElement(self, element):
		self.elements.append(element)
		if len(self.elements) == 1:
			self.setSelectedIndex(0)
		else:
			element.onLoseFocus()
	
	def tabNext(self):
		nextIdx = (self.currentIdx + 1) % len(self.elements)
		self.setSelectedIndex(nextIdx)
		return self.currentElement
		
	def tabPrev(self):
		prevIdx = (self.currentIdx - 1) % len(self.elements)
		self.setSelectedIndex(prevIdx)
		return self.currentElement
	
	def setSelectedIndex(self, idx):
		if idx < 0 or idx >= len(self.elements):
			raise IndexError("element index out of range")
		if self.currentElement is not None:
			self.currentElement.onLoseFocus()
		self.currentIdx = idx
		self.currentElement = self.elements[idx]
		self.currentElement.onFocus()
	
	def onInput(self, inputChar):
		if inputChar == ord('\t'):
			self.tabNext()
			return None
		elif inputChar == curses.KEY_BACKSPACE:
			self.tabPrev()
			return None
		returnValue =  self.currentElement.onInput(inputChar)
		if returnValue == "TAB_NEXT":
			self.tabNext()
			return None
		return returnValue