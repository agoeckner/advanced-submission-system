#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import shutil
import GradeInterface
import CourseManager
import ConfigManager
import GradeConfigManager
import SubmissionManager

class AdvancedSubmissionSystem:
	#GLOBAL_PATH = "/etc/submission/global.config"
	GLOBAL_PATH = "./global.config"
	gradeUI = None
	courseManager = None
	configManager = None
	gradeManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		
		mode = GradeInterface.MODE_STUDENT
		# TODO: This is temporary, for testing.
		# TODO: Replace with a user group check to see if professor or student.
		if len(sys.argv) > 1 and sys.argv[1] == "edit":
			mode = GradeInterface.MODE_INSTRUCTOR
		
		self.configManager = ConfigManager.ConfigManager()
		self.gradeManager = GradeConfigManager.GradeConfigManager()
		courseManager = CourseManager.CourseManager(self)
		
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		self.courseManager = CourseManager.CourseManager(self)
		self.gradeUI = GradeInterface.GradeInterface(self, mode)
		
		self.setUp()
		try:
			self.gradeUI.show()
		except KeyboardInterrupt:
			print("Exited")
	
		self.takeDown()
	
	def setUp(self): #{
		os.mkdir("./courses")
		configFile = open("./global.config", "w")
		configFile.close()
		
		self.configManager.addInstructor(self.GLOBAL_PATH, "Instructors")
		self.courseManager.createCourse("./courses/", "cs180", "cs180Users")
		self.courseManager.createCourse("./courses/", "cs240", "cs240Users")
	#}
	
	def takeDown(self): #{
		shutil.rmtree("./courses")
		os.remove("./global.config")
	#}
	
# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()