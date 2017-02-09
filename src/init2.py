#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os
import sys
import AddGradesInterface
import AddGradesManager

class AdvancedSubmissionSystem:
	addGradesManager = None
	addGradesUI = None

	# Perform program initialization.
	def __init__(self):
		# Fix for ncurses over PuTTY.
		os.environ["NCURSES_NO_UTF8_ACS"] = "1"
		# Setup
		self.addGradesManager = AddGradesManager.AddGradesManager(self)
		self.addGradesUI = AddGradesInterface.AddGradesInterface(self)
		try:
			self.addGradesUI.show()
		except KeyboardInterrupt:
			print("Nothing was saved.")

# Start the program.
if __name__ == '__main__':
	AdvancedSubmissionSystem()