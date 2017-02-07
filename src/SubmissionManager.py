#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

# SubmissionManager handles the actual submission of assignments.
class SubmissionManager:
	parent = None
	def __init__(self, parent):
		self.parent = parent
	
	# Returns a list of available courses.
	def getCourseList(self):
		# TODO: Actually write this function!
		return ["cs180", "cs240", "cs250", "cs251", "cs252", "cs354", "cs307",
			"cs422", "cs408"]