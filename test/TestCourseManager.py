#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import curses
import ConfigManager
import CourseManager
import GradeConfigManager
import os
import shutil



class TestCourseManager(unittest.TestCase): #{
	GLOBAL_PATH = "./global.config"
	
	def setUp(self): #{
		self.configManager = ConfigManager.ConfigManager()
		self.courseManager = CourseManager.CourseManager(self)
		self.gradeManager = GradeConfigManager.GradeConfigManager()
		
		os.mkdir("./courses")
		configFile = open("./global.config", "w")
		configFile.close()
		
	#}
	
	def tearDown(self): #{
		shutil.rmtree("./courses")
		os.remove("./global.config")
	#}
	
	
	##-------------------------------------------------------------------------
	## Test cases for creating a course
	##-------------------------------------------------------------------------
	def test_create_course_1(self): #{
		check = self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		self.assertEqual(check, True)
	#}
	
	def test_create_course_2(self): #{
		check = self.courseManager.createCourse("./courses/", "cs180", "cs180Users")
		
		self.assertEqual(check, True)
	#}
	
	def test_create_course_3(self): #{
		check = self.courseManager.createCourse("./courses/", "cs252", "cs252Users")
		
		self.assertEqual(check, True)
	#}
	
	def test_create_course_already_exists_1(self): #{
		check = self.courseManager.createCourse("./courses/", "cs251", "cs251Users")
		self.assertEqual(check, True)
		
		check = self.courseManager.createCourse("./courses/", "cs251", "cs251Users")
		
		self.assertEqual(check, False)
	#}
	
	def test_create_course_already_exists_2(self): #{
		check = self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.assertEqual(check, True)
		
		check = self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		self.assertEqual(check, False)
	#}
	
	def test_create_course_already_exists_3(self): #{
		check = self.courseManager.createCourse("./courses/", "cs354", "cs354Users")
		self.assertEqual(check, True)
		
		check = self.courseManager.createCourse("./courses/", "cs354", "cs354Users")
		
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for deleting a course
	##-------------------------------------------------------------------------
	def test_delete_course_1(self): #{
		self.courseManager.createCourse("./courses/", "cs354", "cs354Users")
		
		check = self.courseManager.deleteCourse("cs354")
		
		self.assertEqual(check, True)
	#}
	
	def test_delete_course_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		check = self.courseManager.deleteCourse("cs240")
		
		self.assertEqual(check, True)
	#}
	
	def test_delete_course_3(self): #{
		self.courseManager.createCourse("./courses/", "cs252", "cs252Users")
		
		check = self.courseManager.deleteCourse("cs252")
		
		self.assertEqual(check, True)
	#}
	
	def test_delete_course_does_not_exist_1(self): #{
		check = self.courseManager.deleteCourse("cs252")
		
		self.assertEqual(check, False)
	#}
	
	def test_delete_course_does_not_exist_2(self): #{
		check = self.courseManager.deleteCourse("cs180")
		
		self.assertEqual(check, False)
	#}
	
	def test_delete_course_does_not_exist_3(self): #{
		check = self.courseManager.deleteCourse("cs240")
		
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for creating an assignment
	##-------------------------------------------------------------------------
	def test_create_assignment_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		check = self.courseManager.createAssignment("cs240", "Lab1", "2017-03-25", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_2(self): #{
		self.courseManager.createCourse("./courses/", "cs180", "cs240Users")
		check = self.courseManager.createAssignment("cs180", "Lab4", "2017-03-25", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		check = self.courseManager.createAssignment("cs240", "Homework1", "2017-03-25", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_already_exists_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Homework1", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Homework1", "2017-03-25", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	def test_create_assignment_already_exists_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab3", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Lab3", "2017-03-25", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	def test_create_assignment_already_exists_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Project3", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Project3", "2017-03-25", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for deleting an assignment
	##-------------------------------------------------------------------------
	def test_delete_assignment_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Homework5", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.deleteAssignment("Homework5", "cs240")
		self.assertEqual(check, True)
	#}
	
	def test_delete_assignment_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab6", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.deleteAssignment("Lab6", "cs240")
		self.assertEqual(check, True)
	#}
	
	def test_delete_assignment_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Project3", "2017-03-25", False, 3, 3)
		
		check = self.courseManager.deleteAssignment("Project3", "cs240")
		self.assertEqual(check, True)
	#}
	
	def test_delete_assignment_does_not_exist_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		check = self.courseManager.deleteAssignment("Lab2", "cs240")
		self.assertEqual(check, False)
	#}
	
	def test_delete_assignment_does_not_exist_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		check = self.courseManager.deleteAssignment("Project1", "cs240")
		self.assertEqual(check, False)
	#}
	
	def test_delete_assignment_does_not_exist_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		check = self.courseManager.deleteAssignment("Homework3", "cs240")
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for modifying an assignment's details
	##-------------------------------------------------------------------------
	def test_modify_assignment_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Homework5", "2017-03-25", False, 3, 3)
		self.courseManager.modifyAssignment("cs240", "Homework5", "due", "04/25/2017")
		
		check = self.courseManager.getAssignmentSetting("cs240", "Homework5", "due")
		self.assertEqual(check, "04/25/2017")
	#}
	
	def test_modify_assignment_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Project3", "2017-04-05", False, 3, 3)
		self.courseManager.modifyAssignment("cs240", "Project3", "max_submissions", 5)
		
		check = self.courseManager.getAssignmentSetting("cs240", "Project3", "max_submissions")
		self.assertEqual(check, "5")
	#}
	
	def test_modify_assignment_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab2", "2017-04-05", False, 3, 3)
		self.courseManager.modifyAssignment("cs240", "Lab2", "late days", 4)
		
		check = self.courseManager.getAssignmentSetting("cs240", "Lab2", "late days")
		self.assertEqual(check, "4")
	#}
	
	def test_modify_assignment_4(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.modifyAssignment("cs240", "Lab4", "team", "True")
		
		check = self.courseManager.getAssignmentSetting("cs240", "Lab4", "team")
		self.assertEqual(check, "True")
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for enterGrade
	##-------------------------------------------------------------------------
	def test_enter_grade_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		
		check = self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 100, 15, "Job well done lad")
		
		self.assertEqual(check, True)
	#}
	
	def test_enter_grade_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		
		check = self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 80, 15, "Not to shabby")
		
		self.assertEqual(check, True)
	#}
	
	def test_enter_grade_does_not_exist_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		
		check = self.courseManager.enterGrade("cs240", "Lab4", "johndoe", 100, 15, "Job well done lad")
		
		self.assertEqual(check, False)
	#}
	
	def test_enter_grade_does_not_exist_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		
		check = self.courseManager.enterGrade("cs240", "Lab4", "janedoe", 50, 5, "Need to work harder on assignments")
		
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for getGrade
	##-------------------------------------------------------------------------
	def test_get_grade_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 90, 15, "Not to shabby")
		
		grade = self.courseManager.getGrade("cs240", "Lab4", "smithhe")
		self.assertEqual(grade, "90")
	#}
	
	def test_get_grade_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 95, 15, "Not to shabby")
		
		grade = self.courseManager.getGrade("cs240", "Lab4", "smithhe")
		self.assertEqual(grade, "95")
	#}
	
	def test_get_grade_does_not_exist_1(self): #{
		grade = self.courseManager.getGrade("cs240", "Lab4", "johndoe")
		self.assertEqual(grade, False)
	#}
	
	def test_get_grade_does_not_exist_2(self): #{
		grade = self.courseManager.getGrade("cs240", "Lab4", "matt95")
		self.assertEqual(grade, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for getBonus
	##-------------------------------------------------------------------------
	def test_get_bonus_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 100, 15, "Job well done lad")
		
		bonus = self.courseManager.getBonus("cs240", "Lab4", "smithhe")
		self.assertEqual(bonus, "15")
	#}
	
	def test_get_bonus_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 80, 5, "Job well done lad")
		
		bonus = self.courseManager.getBonus("cs240", "Lab4", "smithhe")
		self.assertEqual(bonus, "5")
	#}
	
	def test_get_bonus_does_not_exist_1(self): #{
		bonus = self.courseManager.getBonus("cs240", "Lab4", "gjohn")
		self.assertEqual(bonus, False)
	#}
	
	def test_get_bonus_does_not_exist_2(self): #{
		bonus = self.courseManager.getBonus("cs240", "Lab4", "lyndonj")
		self.assertEqual(bonus, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for getFeedback
	##-------------------------------------------------------------------------
	def test_get_feedback_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 100, 5, "Job well done lad")
		
		feedback = self.courseManager.getFeedback("cs240", "Lab4", "smithhe")
		self.assertEqual(feedback, "Job well done lad")
	#}
	
	def test_get_feedback_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 80, 5, "Needs some improvement")
		
		feedback = self.courseManager.getFeedback("cs240", "Lab4", "smithhe")
		self.assertEqual(feedback, "Needs some improvement")
	#}
	
	def test_get_feedback_does_not_exist_1(self): #{
		feedback = self.courseManager.getFeedback("cs240", "Lab4", "mehargng")
		self.assertEqual(feedback, False)
	#}
	
	def test_get_feedback_does_not_exist_2(self): #{
		feedback = self.courseManager.getFeedback("cs240", "Lab4", "donahuemp")
		self.assertEqual(feedback, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for editGrade
	##-------------------------------------------------------------------------
	def test_edit_grade_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 80, 5, "Needs some improvement")
		
		check = self.courseManager.editGrade("cs240", "Lab4", "smithhe", 95)
		self.assertEqual(check, True)
	#}
	
	def test_edit_grade_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 90, 5, "Needs some improvement")
		
		check = self.courseManager.editGrade("cs240", "Lab4", "smithhe", 100)
		self.assertEqual(check, True)
	#}
	
	def test_edit_grade_does_not_exist_1(self): #{
		check = self.courseManager.editGrade("cs240", "Lab4", "mehargng", 100)
		self.assertEqual(check, False)
	#}
	
	def test_edit_grade_does_not_exist_2(self): #{
		check = self.courseManager.editGrade("cs240", "Lab4", "donahuemp", 100)
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for editBonus
	##-------------------------------------------------------------------------
	def test_edit_bonus_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 90, 5, "Job well done lad")
		
		check = self.courseManager.editBonus("cs240", "Lab4", "smithhe", 10)
		self.assertEqual(check, True)
	#}
	
	def test_edit_bonus_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab4", "2017-04-05", False, 3, 3)
		self.courseManager.enterGrade("cs240", "Lab4", "smithhe", 90, 10, "Job well done lad")
		
		check = self.courseManager.editBonus("cs240", "Lab4", "smithhe", 15)
		self.assertEqual(check, True)
	#}
	
	def test_edit_bonus_does_not_exist_1(self): #{
		check = self.courseManager.editBonus("cs240", "Lab4", "mehargng", 15)
		self.assertEqual(check, False)
	#}
	
	def test_edit_bonus_does_not_exist_2(self): #{
		check = self.courseManager.editBonus("cs240", "Lab4", "donahuemp", 15)
		self.assertEqual(check, False)
	#}
#}

if __name__ == '__main__':
	unittest.main()














