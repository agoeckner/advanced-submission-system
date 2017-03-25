#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import os, pwd, grp, sys, tarfile
import shutil
import ConfigManager
import locale
import time
from datetime import datetime

# SubmissionManager handles the actual submission of assignments.
class SubmissionManager:
	parent = None
	def __init__(self, parent):
		self.parent = parent
		self.manager = ConfigManager.ConfigManager()
	
	# Returns a list of available courses.
	def getCourseList(self):
		return self.manager.getCourseList(self.parent.GLOBAL_PATH)
	
	# Returns a list of available projects in a course.
	def getAssignmentList(self, course):
		return self.manager.getProjects(self.manager.get_setting(self.parent.GLOBAL_PATH, course, "course_config_file"))
	
	# Submits an assignment.
	# course, assignment are strings
	# files is a list of file strings
	# Return true on success, false on failure
	def submitAssignment(self, course, assignment, files):

		#groups is a list of all groups the user belongs to
		#raise Exception(files)
		
		user = pwd.getpwuid(os.getuid()).pw_name
		groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
		gid = pwd.getpwnam(user).pw_gid
		groups.append(grp.getgrgid(gid).gr_name)
		
		#if course isn't in groups, user isn't in the class
		courseGroup = self.manager.get_setting(self.parent.GLOBAL_PATH, course, "user_group")
		#if (courseGroup) not in groups:
		if (0): 
			print('You do not have access to that course')
			return False
		
		#Compare Submission date to due date

		today = datetime.now()
		courseName = self.parent.courseManager.courseNameToPath(course) + "/";
		projectDueDate = self.manager.getProjectInfo(courseName + self.manager.get_setting(self.parent.GLOBAL_PATH, course, "course_config_file"), assignment, "due") 
		dueDateString = str(projectDueDate)
		dueDate = datetime.strptime(dueDateString, "%Y-%m-%d %H:%M:%S")
		if dueDate <= today:
			print("You cannot submit files past the deadline")
			return False
		

		#file path to submit files
		path = self.manager.get_setting(self.parent.GLOBAL_PATH, course, "course_path") + '/' + assignment + '/' + user + '/'

		#Check for earlier submissions

		count = 0
		while os.path.isfile(path + '/submission' + str(count) + '.tar.gz'):
			count += 1


		#Check max submissions
		maxSubmissions = int(self.manager.getProjectInfo(courseName + self.manager.get_setting(self.parent.GLOBAL_PATH, course, "course_config_file"), assignment, "max_submissions"))
		if count > maxSubmissions:
			print('You have already submitted the maximum number of attempts')
			return False

		submission = 'submission' + str(count) + '.tar.gz'
		tar = tarfile.open(submission, 'w:gz')

		for f in files:
			try:
				tar.add(f)
			except:
				#raise Exception(f)
				print('file ' + f + ' not found')

		
		if not os.path.exists(path):
			os.makedirs(path)
		shutil.move('submission' + str(count) + '.tar.gz', path)
		return True
		
def main():
	sm = SubmissionManager(None)
	files = ['ConfigManager.py', 'CourseManager.py']
	print()
	
	print("**** 1st Test - Correctly Submitted assignment ****")
	if (sm.submitAssignment("CS180", "lab1", files) == True):
		print("Test 1 Passed")
	else:
		print("Test1 Failed")

	print()

	print("**** 2nd Test - Submitting past Max Submissions ****")

	sm.submitAssignment("CS180", "project1", files) 
	if (sm.submitAssignment("CS180", "project1", files) == False):
		print("Test 2 Passed")
	else:
		print("Test 2 Failed")
	
	print()
	print("**** 3rd Test - Submimtting after Due Date ****")
	
	if (sm.submitAssignment("CS240", "lab1", files) == False):
		print("Test 3 Passed")
	else:
		print("Test 3 Failed")

	print()
	print("**** 4th Test - Submitting in wrong class ****")
	
	if (sm.submitAssignment("CS252", "HomeWork1", files) == False):
		print("Test 4 Passed")
	else:
		print("Test 4 Failed")

	
	

if __name__ == '__main__':
	main()
