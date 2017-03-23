#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import grp
import pwd
import shutil
import GradeInterface
import CourseManager
import ConfigManager
import GradeConfigManager
import SubmissionManager

class AdvancedSubmissionSystem:
	GLOBAL_PATH = "/etc/submission/global.config"
	gradeUI = None
	courseManager = None
	configManager = None
	gradeManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		
		self.configManager = ConfigManager.ConfigManager()
		self.gradeManager = GradeConfigManager.GradeConfigManager()
		self.courseManager = CourseManager.CourseManager(self)
		
		user = pwd.getpwuid(os.getuid()).pw_name
		groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]

		mode = GradeInterface.MODE_STUDENT
		if self.configManager.getInstructorGroup(self.GLOBAL_PATH) in groups:
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