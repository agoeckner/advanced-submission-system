
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
		correct test student and the number of iteration of the for loops
		below should match the actual courses, proeccts and files the tester is already aware of
		'''
		# go to the intended course with left arrow
		for i in range(3):
			self.inputMgr.onInput(curses.KEY_DOWN)
		# select the course with enter
		self.inputMgr.onInput(ord('\n'))

		# go to the intended project with left arrow
		for i in range(3):
			self.inputMgr.onInput(curses.KEY_DOWN)
		# select the project with enter
		self.inputMgr.onInput(ord('\n'))

		# select a single file
		for i in range():
			self.inputMgr.onInput(curses.KEY_DOWN)
		# select the file with enter
		self.inputMgr.onInput(ord('\n'))

		# select submit
		self.inputMgr.onInput(ord('\n'))

		# now we can check if the file was actually submitted
		dest = 'path/to/the/submission/dir/<already known filename>'
		my_file = Path(dest)
		# verify the file is submitted 
		self.assertTrue( my_file.is_file() )
		


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

