#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import curses
import ui.InputManager as InputManager

class TestUIInputManager(unittest.TestCase):
	def setUp(self):
		self.inputMgr = InputManager.InputManager(None)
		self.e1 = StubElement()
		self.e2 = StubElement()
		self.e3 = StubElement()
		self.inputMgr.addElement(self.e1)
		self.inputMgr.addElement(self.e2)
		self.inputMgr.addElement(self.e3)
		
	def test_add_elements(self):
		self.assertEqual(self.inputMgr.elements, [self.e1, self.e2, self.e3])
	
	def test_auto_select_after_add(self):
		self.assertEqual(self.inputMgr.currentElement, self.e1)
	
	def test_tabnext_nowrap(self):
		self.inputMgr.tabNext()
		self.assertEqual(self.inputMgr.currentElement, self.e2)

	def test_tabnext_wrap(self):
		self.inputMgr.tabNext()
		self.inputMgr.tabNext()
		self.inputMgr.tabNext()
		self.assertEqual(self.inputMgr.currentElement, self.e1)

	def test_tabprev_wrap(self):
		self.inputMgr.tabPrev()
		self.assertEqual(self.inputMgr.currentElement, self.e3)

	def test_select_valid(self):
		self.inputMgr.setSelectedIndex(1)
		self.assertEqual(self.inputMgr.currentElement, self.e2)

	def test_select_invalid_high(self):
		with self.assertRaises(IndexError):
			self.inputMgr.setSelectedIndex(3)

	def test_select_invalid_low(self):
		with self.assertRaises(IndexError):
			self.inputMgr.setSelectedIndex(-1)

	def test_input_next(self):
		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e2)
		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e3)
	
	def test_input_prev(self):
		self.inputMgr.onInput(curses.KEY_BACKSPACE)
		self.assertEqual(self.inputMgr.currentElement, self.e3)
		self.inputMgr.onInput(curses.KEY_BACKSPACE)
		self.assertEqual(self.inputMgr.currentElement, self.e2)
	
	def test_input_next_prev(self):
		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e2)
		self.inputMgr.onInput(curses.KEY_BACKSPACE)
		self.assertEqual(self.inputMgr.currentElement, self.e1)

	def test_input_prev_next(self):
		self.inputMgr.onInput(curses.KEY_BACKSPACE)
		self.assertEqual(self.inputMgr.currentElement, self.e3)
		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e1)

	def test_input_select_autoadvance(self):
		self.inputMgr.onInput(ord('a'))
		self.assertEqual(self.inputMgr.currentElement, self.e2)

class StubElement:
	def onLoseFocus(self):
		pass
	
	def onFocus(self):
		pass
	
	def onInput(self, inputChar):
		return "TAB_NEXT"

if __name__ == '__main__':
	unittest.main()