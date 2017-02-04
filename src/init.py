#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import SubmissionInterface

class AdvancedSubmissionSystem:
	# Perform program initialization.
	def __init__(self):
		submissionUI = SubmissionInterface.SubmissionInterface()
		try:
			submissionUI.show()
		except KeyboardInterrupt:
			print("WARNING: Nothing was submitted!")

	# Perform 

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()