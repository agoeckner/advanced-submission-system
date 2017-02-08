#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os, pwd, grp, sys, tarfile

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
	def submitAssignment(self, course, assignment, files):
		#groups is a list of all groups the user belongs to
		'''
		goups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
		gid = pwd.getpwnam(user).pw_gid
		groups.append(grp.getgrgid(gid).gr_name)
		
		#if course isn't in groups, user isn't in the class
		if course not in groups:
			print('You do not have access to ' + course)
			return False
		'''
		tar = tarfile.open('submission.tar.gz', 'w:gz')

		#TODO: parse config file to locate path
		path = ''

		for f in files:
			try:
				tar.add(f)
				break
			except RuntimeError:
				print('file ' + f + ' not found')

		print('zipping files to ' + path)
		
		#uncomment when all is done
		#shutil.move('submission.tar.gz', path)
		return True
		
