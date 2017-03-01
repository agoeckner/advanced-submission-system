#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import GradeInterface
import SubmissionInterface
import SubmissionManager
import CourseManager

GLOBAL_PATH = "/etc/submission/global.config"

class AdvancedSubmissionSystem:
	submissionManager = None
	submissionUI = None
	courseManager = None
	
	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		
		# Set up the backend.
		self.courseManager = CourseManager.CourseManager(self)
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		
		# Grade Interface
		if len(sys.argv) > 1 and sys.argv[1] == "grades":
			self.gradeUI = GradeInterface.GradeInterface(self, GradeInterface.MODE_STUDENT)
			try:
				self.gradeUI.show()
			except KeyboardInterrupt:
				print("Goodbye!")
		# Course Manager Testing?
		elif len(sys.argv) > 1 and sys.argv[1] == "course":
			self.courseManager.start()
		# Submission Interface
		else:
			self.submissionUI = SubmissionInterface.SubmissionInterface(self)
			try:
				self.submissionUI.show()
			except KeyboardInterrupt:
				print("WARNING: Nothing was submitted!")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()