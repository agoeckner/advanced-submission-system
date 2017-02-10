#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import ui.InputManager as InputManager

class TestUIInputManager(unittest.TestCase):
	def setUp(self):
		self.inputMgr = InputManager.InputManager(None)
		self.e1 = StubElement()
		self.e2 = StubElement()
		self.e3 = StubElement()
	
	def tearDown(self):
		self.inputMgr = None
		self.e1 = None
		self.e2 = None
		self.e3 = None
		
	def test_add_elements(self):
		self.inputMgr.addElement(self.e1)
		self.inputMgr.addElement(self.e2)
		self.inputMgr.addElement(self.e3)
		self.assertEqual(self.inputMgr.elements, [self.e1, self.e2, self.e3])
	
	def test_auto_select_after_add(self):
		self.inputMgr.addElement(self.e1)
		self.inputMgr.addElement(self.e2)
		self.inputMgr.addElement(self.e3)
		self.assertEqual(self.inputMgr.currentElement, self.e1)
	
	def test_tabnext_nowrap(self):
		# self.inputMgr.addElement(self.e1)
		# self.inputMgr.addElement(self.e2)
		self.inputMgr.tabNext()
		self.assertEqual(self.inputMgr.currentElement, self.e2)

	def test_tabnext_wrap(self):
		self.inputMgr.tabNext()
		self.inputMgr.tabNext()
		self.assertEqual(self.inputMgr.currentElement, self.e1)

	def test_tabprev_wrap(self):
		self.inputMgr.tabPrev()
		self.assertEqual(self.inputMgr.currentElement, self.e3)

	def test_select_valid(self):
		self.inputMgr.setSelectedIndex(0)
		self.assertEqual(self.inputMgr.currentElement, self.e1)

	def test_select_invalid_high(self):
		with self.assertRaises(IndexError):
			self.inputMgr.setSelectedIndex(3)

	def test_select_invalid_low(self):
		with self.assertRaises(IndexError):
			self.inputMgr.setSelectedIndex(-1)

class StubElement:
	def onLoseFocus(self):
		pass
	
	def onFocus(self):
		pass
	
	def onInput(self, inputChar):
		return None

if __name__ == '__main__':
	unittest.main()