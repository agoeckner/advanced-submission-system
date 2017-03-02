import locale
import os
import shutil
import ConfigManager
import configparser

class CourseManager:
	manager = None
	parent = None
	
	
	##constructor
	def __init__(self, parent): #{
		self.parent = parent
		self.manager = self.parent.configManager
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code that is used for creating and deleting courses
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##creates a new course directory
	##path is the path to where the course directory is to be created
	##courseName is the name of the new course
	def createCourse(self, path, courseName, userGroup): #{
		##Create a new directory for the courseName
		newCoursePath = path + courseName
		
		if os.path.exists(newCoursePath):
			#print("Course already exists")
			return False
		
		try:
			self.addFolder(newCoursePath)
		except OSError: 
			return False
		
		courseConfigFile = newCoursePath + "/course.config" ##creates the course config file
		
		##create the course config file
		try:
			configFile = open(courseConfigFile, "w")
			configFile.close()
		except:
			return False
		
		##updates the global config
		check = self.manager.addCourse("./global.config", courseName, courseConfigFile, newCoursePath, userGroup)
		
		##if the course config file is not created False is returned to indicate an error
		if check == False:
			return False
		
		return True
	#}

	##deletes a course directory in the instructor's directory
	##courseName is the name of the course to be removed
	def deleteCourse(self, courseName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False

		courseConfigFile = path + "/course.config"
		
		check = self.manager.removeCourse(courseConfigFile, "global.config", courseName) ##removes the course from the global config file
		
		if not check: #{
			return False
		#}
		
		self.deleteFolder(path) ##deletes the course and all assignments under it
		
		return True
	#}
	
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code that is used for creating and deleting assignments 
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##creates a new assignment directory inside the course directory
	##assignmentName is the name of the new directory
	##courseName is the name of the course, assignmentName is the name of the assignment, dueDate is the day the assignment is dueDate
	##team identifies if the assignment is a team assignment, maxSubmissions are the total number of submissions allowed, lateDays are the 
	##number of days allowed for late submission
	def createAssignment(self, courseName, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		assignmentPath = path + "/" + assignmentName
		
		
		if os.path.exists(assignmentPath):
			#print("Assignment already exists")
			return False
		
		try:
			self.addFolder(assignmentPath) ##creates a new folder for the assignment
		except OSError:
			return False
		
		assignmentConfigFile = assignmentPath + "/assignment.config"
		
		##create the assignment config file
		try:
			configFile = open(assignmentConfigFile, "w")
			configFile.close()
		except:
			return False
		
		##adds the assignment to the global config file
		check = self.parent.configManager.addProject(assignmentConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		if not check:
			return False
		
		##Create all the student directories

		return True
	#}

	##deletes the assignment specified by assignmentName
	##assignmentName is the assignment to be deleted
	##courseName is the name of the course
	def deleteAssignment(self, assignmentName, courseName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		courseConfigFile = path + "/course.config"
		
		##removes the assignment from the course config file
		check = self.parent.configManager.removeProject(courseConfigFile, assignmentName)
		if not check:
			return False
		
		##removes the directory and all subdirectories and files
		assignmentPath = path + "/" + assignmentName
		try:
			self.deleteFolder(assignmentPath)
		except OSError:
			return False
		
		return True
	#}

	##modifes the config file of an existing assignment
	##assignmentName is the name of the new directory
	##courseName is the name of the course, assignmentName is the name of the assignment, dueDate is the day the assignment is dueDate
	##team identifies if the assignment is a team assignment, maxSubmissions are the total number of submissions allowed, lateDays are the 
	##number of days allowed for late submission
	def modifyAssignment(self, courseName, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		path = parent.ConfigParser.get_setting(GLOBAL_PATH, courseName, "course_path")
		
		courseConfigFile = path + "course.config"
		
		parent.ConfigParser.modifyProject(courseConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		
		return True
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	##  Section of code that is used for grading
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##Gives a grade to the student
	##courseName is the name of the course
	##assignmentName is the name of the assignment, studentName is the name of the student being graded
	##gradeRecieved is the grade recieved for the assignment
	def enterGrade(self, courseName, assignmentName, studentName, gradeRecieved): #{
		path = parent.ConfigParser.get_setting(GLOBAL_PATH, courseName, "course_path")
		
		gradeFile = path + "grade.txt"
		
		grade = open(gradeFile, "w")
		
		grade.write("Grade Recieved: " + gradeRecieved)
		
		grade.close()
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code that is used for creating folders
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##x is the path including the new directory name
	def addFolder(self, x): #{
		##NOTE!-------------------------------------------------------------------------------------
		## mkdir has another parameter that sets permissions for the new directory
		##!-----------------------------------------------------------------------------------------
		os.mkdir(x) ##a new directory is made
	#}

	def deleteFolder(self, x): #{
		shutil.rmtree(x) ##removes the directory and all directories and files inside it
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code for GUI Functionalilty
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	def courseNameToPath(self, courseName): #{
		path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		return path
	#}










