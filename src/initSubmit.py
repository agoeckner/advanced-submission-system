#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import SubmissionInterface
import SubmissionManager
import CourseManager
import ConfigManager


class AdvancedSubmissionSystem:
	GLOBAL_PATH = "/etc/submission/global.config"
	submissionManager = None
	submissionUI = None
	configManager = None
	courseManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		self.configManager = ConfigManager.ConfigManager()
		self.courseManager = CourseManager.CourseManager(self)
		self.submissionUI = SubmissionInterface.SubmissionInterface(self)
		try:
			self.submissionUI.show()
		except KeyboardInterrupt:
			print("WARNING: Nothing was submitted!")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()
