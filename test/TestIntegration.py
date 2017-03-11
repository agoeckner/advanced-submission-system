import sys
sys.path.append('../src/')
import unittest
import curses
import ui.InputManager as InputManager
import ConfigManager
import CourseManager
import GradeConfigManager
import os
import shutil

##--------------------------------------------------------------------------------------------
##All automated test cases must be run on a specific computer to pass
##--------------------------------------------------------------------------------------------

class TestIntegration(unittest.TestCase):
	GLOBAL_PATH = "./global.config"

	def setUp(self):
		self.inputMgr = InputManager.InputManager(None)
		self.e1 = StubElement()
		self.e2 = StubElement()
		self.e3 = StubElement()
		self.inputMgr.addElement(self.e1)
		self.inputMgr.addElement(self.e2)
		self.inputMgr.addElement(self.e3)
		
		self.configManager = ConfigManager.ConfigManager()
		self.courseManager = CourseManager.CourseManager(self)
		self.gradeManager = GradeConfigManager.GradeConfigManager()
		
		os.mkdir("./courses")
		configFile = open("./global.config", "w")
		configFile.close()
		
		self.courseManager.createCourse("./courses/", "cs180", "cs180Users")
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
	
	def tearDown(self): #{
		shutil.rmtree("./courses")
		os.remove("./global.config")
	#}
	
	
	
	def test_create_assignment_1(self): #{
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput(curses.KEY_DOWN)
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput("Homework1")
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput("2017-04-04")
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput("5")
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput("5")
		self.inputMgr.onInput(ord('\n'))
		self.inputMgr.onInput(ord('\n'))
		
		path = "./courses/cs180/Homework1"
		check = os.path.exists(path)
		self.assertEqual(check, True)
	#}
	
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

