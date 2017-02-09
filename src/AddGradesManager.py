#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os, pwd, grp, sys

# AddGradesManager handles the actual submission of assignments.
class AddGradesManager:
	parent = None
	def __init__(self, parent):
		self.parent = parent
	
	# Returns a list of available courses.
	def getCourseList(self):
		# TODO: Actually write this function!
		return ["cs180", "cs240", "cs250", "cs251", "cs252", "cs354", "cs307",
			"cs422", "cs408"]
	
	# Returns a list of available projects in a course.
	def getAssignmentList(self, course):
		# TODO: Actually write this function!
		if course == "cs408":
			return ["project-charter", "backlog", "test-plan", "design-review", "midterm"]
		return ["lab1", "lab2", "homework1", "homework2", "exam1", "final-practice"]
	
	# Submits an assignment.
	# course, assignment are strings
	# files is a list of file strings
	# Return true on success, false on failure