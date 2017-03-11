
import sys
sys.path.append('../src/')
import unittest
import curses
import ui.InputManager as InputManager

class TestIntegration(unittest.TestCase):

	def setUp(self):
		self.inputMgr = InputManager.InputManager(None)
		self.e1 = StubElement()
		self.e2 = StubElement()
		self.e3 = StubElement()
		self.inputMgr.addElement(self.e1)
		self.inputMgr.addElement(self.e2)
		self.inputMgr.addElement(self.e3)
	
	def test_singleSubmission(self):
		'''
		Some assumptions required. User should be logged in as the
		correct test student
		'''
		# go to the course with left arrow
		for i in range(3):
			self.inputMgr.onInput(curses.KEY_DOWN)
		# select the course with enter
		self.inputMgr.onInput(ord('\n'))

		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e2)
		self.inputMgr.onInput(ord('\t'))
		self.assertEqual(self.inputMgr.currentElement, self.e3)	


class StubElement:
	def onLoseFocus(self):
		pass	
	def onFocus(self):
		pass	
	def onInput(self, inputChar):
		return "TAB_NEXT"

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegration)
	unittest.TextTestRunner(verbosity=2).run(suite)

