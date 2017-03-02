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
import os
import shutil



class TestCourseManager(unittest.TestCase): #{
	GLOBAL_PATH = "./global.config"
	
	def setUp(self): #{
		self.configManager = ConfigManager.ConfigManager()
		self.courseManager = CourseManager.CourseManager(self)
		
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
		check = self.courseManager.createAssignment("cs240", "Lab1", "03/21/2017", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_2(self): #{
		self.courseManager.createCourse("./courses/", "cs180", "cs240Users")
		check = self.courseManager.createAssignment("cs180", "Lab4", "04/22/2017", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		check = self.courseManager.createAssignment("cs240", "Homework1", "05/02/2017", False, 3, 3)
		
		self.assertEqual(check, True)
	#}
	
	def test_create_assignment_already_exists_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Homework1", "05/02/2017", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Homework1", "05/02/2017", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	def test_create_assignment_already_exists_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab3", "03/02/2017", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Lab3", "03/02/2017", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	def test_create_assignment_already_exists_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Project3", "03/25/2017", False, 3, 3)
		
		check = self.courseManager.createAssignment("cs240", "Project3", "03/25/2017", False, 3, 3)
		self.assertEqual(check, False)
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for deleting an assignment
	##-------------------------------------------------------------------------
	def test_delete_assignment_1(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Homework5", "03/25/2017", False, 3, 3)
		
		check = self.courseManager.deleteAssignment("Homework5", "cs240")
		self.assertEqual(check, True)
	#}
	
	def test_delete_assignment_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Lab6", "03/25/2017", False, 3, 3)
		
		check = self.courseManager.deleteAssignment("Lab6", "cs240")
		self.assertEqual(check, True)
	#}
	
	def test_delete_assignment_3(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		self.courseManager.createAssignment("cs240", "Project3", "03/25/2017", False, 3, 3)
		
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
#}

if __name__ == '__main__':
	unittest.main()














