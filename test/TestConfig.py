import sys
import optparse
import os
import configparser
sys.path.append('../src/')

import ConfigManager
import unittest

'''
run using :  python -m unittest -v  TestConfig
'''
class TestConfigManager(unittest.TestCase):

	def setUp(self):
		path_to_repo = os.environ['HOME'] + "/cs408"
		self.cm = ConfigManager.ConfigManager()
		self.validCourseConfig = path_to_repo + "/advanced-submission-system/test/testCourse/testCourse.config"
		self.validGlobalConfig = path_to_repo + "/advanced-submission-system/test/testGlobal.config"

	def test_invalidDate(self):
		invalidDate = '1254698'
		self.assertFalse(self.cm.addCourse("global.cof", "cs999", 
			"/dir/path/file", "profK/cs999/", "std") )		
		
	def test_invalidProject(self):
		invalidFile = "doesntExist.conf"
		with self.assertRaises(Exception):
			self.cm.getProjectInfo(invalidFile, "prj1")
	
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
		self.assertEqual(self.cm.getCourseList(invalidFile), {} )

	def test_getSettingValid(self):
		returnedVal = self.cm.get_setting(self.validCourseConfig, "project1", "max_submissions")
		self.assertEqual(returnedVal, "5")

	def test_removeCourseInvalid(self):
		self.assertFalse(self.cm.removeCourse( "invalidFile.config", "invalidGlobal.config", "proj1"))

	def test_getProjectInfo(self):
		projInfo = self.cm.getProjectInfo(self.validCourseConfig, 'project1')
		print( str(projInfo) )
		self.assertTrue('False' in projInfo[0]) # test team proj boolean
		self.assertTrue('5' in projInfo[1]) # test mac submissions
		#self.assertTrue('2018-12-15 00:00:00' in projInfo) # testdue date
		#self.assertTrue('late days' in projInfo) # test late days


	def test_courseList(self):
		res = self.cm.getCourseList(self.validGlobalConfig)
		self.assertTrue("cs242" in res)
		self.assertTrue("cs240" in res)
		self.assertTrue("cs243" in res)
		self.assertTrue("cs241" in res)
	def test_addInstructor(self):
		self.cm.addInstructor(self.validGlobalConfig, 'instructors_spring17')
		res = self.cm.getInstructorGroup(self.validGlobalConfig)
		self.assertTrue('instructors_spring17' in res);

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigManager)
	unittest.TextTestRunner(verbosity=2).run(suite)

