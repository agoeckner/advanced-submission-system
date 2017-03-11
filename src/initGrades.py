#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import grp
import pwd
import GradeInterface
import CourseManager
import ConfigManager
import GradeConfigManager

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
		
		self.gradeUI = GradeInterface.GradeInterface(self, mode)
		try:
			self.gradeUI.show()
		except KeyboardInterrupt:
			print("Exited")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()