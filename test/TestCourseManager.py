#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import curses

class TestCourseManager: #{
	
	def setUp(self): #{
		self.courseManager = CourseManager.CourseManager(self)
		os.mkdir("./courses")
		configFile = open("./global.config", "w")
		configFile.close()
		
	#}
	
	def cleanUp(self): #{
		shutil.rmtree("./courses")
		os.remove("./global.config")
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for creating a course
	##-------------------------------------------------------------------------
	def test_create_course_1(self): #{
		check = self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		self.assertEqual(check, True)
		self.self.cleanUp()
	}
	
	def test_create_course_2(self): #{
		check = self.courseManager.createCourse("./courses/", "cs180", "cs180Users")
		
		self.assertEqual(check, True)
		self.self.cleanUp()
	}
	
	def test_create_course_3(self): #{
		check = self.courseManager.createCourse("./courses/", "cs252", "cs252Users")
		
		self.assertEqual(check, True)
		self.self.cleanUp()
	}
	
	def test_create_course_already_exists_1(self): #{
		self.courseManager.createCourse("./courses/", "cs251", "cs251Users")
		
		check = self.courseManager.createCourse("./courses/", "cs251", "cs251Users")
		
		self.assertEqual(check, False)
		self.cleanUp()
	#}
	
	def test_create_course_already_exists_2(self): #{
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		check = self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
		
		self.assertEqual(check, False)
		self.cleanUp()
	#}
	
	def test_create_course_already_exists_3(self): #{
		self.courseManager.createCourse("./courses/", "cs354", "cs354Users")
		
		check = self.courseManager.createCourse("./courses/", "cs354", "cs354Users")
		
		self.assertEqual(check, False)
		self.cleanUp()
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for deleting a course
	##-------------------------------------------------------------------------
	def test_delete_course_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_course_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_course_3(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_course_does_not_exist_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_course_does_not_exist_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_course_does_not_exist_3(self): #{
		
		self.cleanUp()
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for creating an assignment
	##-------------------------------------------------------------------------
	def test_create_assignment_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_create_assignment_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_create_assignment_3(self): #{
		
		self.cleanUp()
	#}
	
	def test_create_assignment_already_exists_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_create_assignment_already_exists_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_create_assignment_already_exists_3(self): #{
		
		self.cleanUp()
	#}
	
	##-------------------------------------------------------------------------
	## Test cases for deleting an assignment
	##-------------------------------------------------------------------------
	def test_delete_assignment_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_assignment_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_assignment_3(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_assignment_does_not_exist_1(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_assignment_does_not_exist_2(self): #{
		
		self.cleanUp()
	#}
	
	def test_delete_assignment_does_not_exist_3(self): #{
		
		self.cleanUp()
	#}
#}















