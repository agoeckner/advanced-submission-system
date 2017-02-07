#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import InstructorInterface

class AdvancedSubmissionSystem:
	# Perform program initialization.
	def __init__(self):
		professorUI = InstructorInterface.InstructorInterface()
		try:
			professorUI.show()
		except KeyboardInterrupt:
			print("Error")

	# Perform 

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()