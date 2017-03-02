#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import StudentInterface
import SubmissionInterface
import SubmissionManager
import CourseManager

GLOBAL_PATH = "/etc/submission/global.config"

class AdvancedSubmissionSystem:
	submissionManager = None
	submissionUI = None
	courseManager = None
	configManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		self.configManager = ConfigManager.ConfigManager()
		
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		self.submissionUI = SubmissionInterface.SubmissionInterface(self)
		try:
			self.submissionUI.show()
		except KeyboardInterrupt:
			print("WARNING: Nothing was submitted!")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()