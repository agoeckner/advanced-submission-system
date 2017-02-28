import sys
sys.path.append('../src/')

import ConfigManager
import unittest

'''
run using :  python -m unittest -v  TestConfig
'''
class TestConfigManager(unittest.TestCase):

	def setUp(self):
		self.cm = ConfigManager.ConfigManager()
		self.validCourseConfig = "../src/testCourse.config"
		self.validGlobalConfig = "../src/testGlobal.config"

	def test_invalidDate(self):
		invalidDate = '1254698'
		self.assertFalse(self.cm.addCourse("global.cof", "cs999", 
			"/dir/path/file", "profK/cs999/", "std") )		
		
	def test_invalidProject(self):
		invalidFile = "doesntExist.conf"		
		self.assertEqual(self.cm.getProjectInfo(invalidFile, "prj1"), None)
	
	def test_getConfFixed(self):
		validFile = self.validCourseConfig
		configObj = self.cm.get_config(validFile)
		self.assertNotEqual(configObj, None)

	def test_removeProjectInvalid(self):
		self.assertFalse(self.cm.removeProject( "invalidFile.config", "proj1"))

	def test_getProjectsInvalid(self):
		invalidFile = "doesntExist.conf"
		with self.assertRaises(Exception):
			self.cm.getProjects(invalidFile, "prj1")

	def test_modifyProjectInvalid(self):
		self.assertFalse( self.cm.modifyProject("invalidFile", "proj1", "12-12-2011", True, 5, 0) )

	def test_getCourseListInvalid(self):
		invalidFile = "doesntExist.conf"
		self.assertEqual(self.cm.getCourseList(invalidFile), None)

	def test_getSettingValid(self):
		returnedVal = self.cm.get_setting(self.validCourseConfig, "project1", "max_submissions")
		self.assertEqual(returnedVal, "5")

	def test_removeCourseInvalid(self):
		self.assertFalse(self.cm.removeCourse( "invalidFile.config", "invalidGlobal.config", "proj1"))

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigManager)
	unittest.TextTestRunner(verbosity=2).run(suite)

