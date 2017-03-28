import sys
import optparse
import os
sys.path.append('../src/')

import GradeConfigManager
import unittest

'''
run using :   python -m unittest -v TestGradeConfigManager
'''
class TestGradeConfigManager(unittest.TestCase):

	def setUp(self):
		path_to_repo = os.environ['HOME'] + "/cs408"
		self.gcm = GradeConfigManager.GradeConfigManager()
		self.test_dir = path_to_repo + "/advanced-submission-system/test/testCourse/testProject"
		self.validGlobalConfig = path_to_repo + "/advanced-submission-system/test/testGlobal.config"
		self.testStudent = path_to_repo + "/advanced-submission-system/test/testCourse/testProject/student1/Grade.config"

	def test_gradeUpdate(self):
		# check if grades are updated
		self.gcm.editGrade( self.testStudent, "87")
		grade = self.gcm.getGrade( self.testStudent)
		self.assertTrue("87" in grade);
		self.gcm.editGrade( self.testStudent, "85")
		grade = self.gcm.getGrade( self.testStudent)
		self.assertTrue("85" in grade);

	def test_feedbackUpdate(self):
		# check if grades are updated
		self.gcm.editFeedback( self.testStudent, "Q1 answer invalid argument")
		grade = self.gcm.getFeedback( self.testStudent)
		#print("-------" +grade)
		self.assertTrue("Q1 answer invalid argument" in grade);
		self.gcm.editFeedback( self.testStudent, "incomplete section 2 & poor report")
		grade = self.gcm.getFeedback( self.testStudent)
		#print("-------" +grade)
		self.assertTrue("incomplete section 2 & poor report" in grade)

	def test_bonusUpdate(self):
		# check if grades are updated
		self.gcm.editBonus( self.testStudent, "5")
		grade = self.gcm.getBonus( self.testStudent)
		#print("-------" +grade)
		self.assertTrue("5" in grade);
		self.gcm.editBonus( self.testStudent, "6")
		grade = self.gcm.getBonus( self.testStudent)
		#print("-------" +grade)
		self.assertTrue("6" in grade)


	def test_basicFunction(self):
		print('Adding grades, bonus and feedback for students1 to 4')

		for subdir, dirs, files in os.walk(self.test_dir):
			for studentDir in dirs:
				gradeConfigFile = os.path.join(subdir, studentDir)
				gradeConfigFile += "/Grade.config"
				if("1" in studentDir):
					self.gcm.addGrade(gradeConfigFile, 85, 6, "incomplete section 2 & poor report")
				elif ("2" in studentDir):
					self.gcm.addGrade(gradeConfigFile, 55, 0, "incomplete report")
				elif ("3" in studentDir):
					self.gcm.addGrade(gradeConfigFile, 70, 13, "prob 1 x = 4 not 15")
				elif ("4" in studentDir):
					self.gcm.addGrade(gradeConfigFile, 0, 0, "no submission")

		rd = self.gcm.getCourseGrades(self.test_dir)
		# grades written into files verify the content is there
		self.assertTrue("student1" in rd.keys() )
		self.assertTrue("student2" in rd.keys() )
		self.assertTrue("student3" in rd.keys() )
		self.assertTrue("student4" in rd.keys() )
		self.assertTrue(rd["student1"] == "Score: 85 Bonus: 6")
		self.assertTrue(rd["student2"] == "Score: 55 Bonus: 0")
		self.assertTrue(rd["student3"] == "Score: 70 Bonus: 13")
		self.assertTrue(rd["student4"] == "Score: 0 Bonus: 0")



if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestGradeConfigManager)
	unittest.TextTestRunner(verbosity=2).run(suite)

