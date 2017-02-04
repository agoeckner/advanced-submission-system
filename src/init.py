#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import SubmissionInterface
import SubmissionManager

class AdvancedSubmissionSystem:
	submissionManager = None
	submissionUI = None

	# Perform program initialization.
	def __init__(self):
		self.submissionManager = SubmissionManager.SubmissionManager(self)
		self.submissionUI = SubmissionInterface.SubmissionInterface(self)
		try:
			self.submissionUI.show()
		except KeyboardInterrupt:
			print("WARNING: Nothing was submitted!")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()