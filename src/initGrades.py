#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import GradeInterface
import SubmissionManager
import CourseManager

GLOBAL_PATH = "/etc/submission/global.config"

class AdvancedSubmissionSystem:
	submissionManager = None
	gradeUI = None
	courseManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		
		mode = GradeInterface.MODE_STUDENT
		# TODO: This is temporary, for testing.
		# TODO: Replace with a user group check to see if professor or student.
		if len(sys.argv) > 1 and sys.argv[1] == "edit":
			mode = GradeInterface.MODE_INSTRUCTOR
		
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		self.gradeUI = GradeInterface.GradeInterface(self, mode)
		try:
			self.gradeUI.show()
		except KeyboardInterrupt:
			print("WARNING: Nothing was submitted!")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()