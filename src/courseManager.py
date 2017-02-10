import locale
import os
import shuttil

class courseManager:
	parent = None
	
	##to get a section for a course
	get_setting(GLOBAL_PATH, courseName, "course_path")
	
	
	
	##TODO: check for existing courses or assignments when creating or deleting
	##TODO: check that the config files are being created after calling configmanager
	
	##constructor
	def __init__(self, parent): #{
		self.parent = parent
	#}
	
''' ----------------------------- Section of code that is used for creating and deleting courses -------------------------------------------'''	
	
	##creates a new course directory in the instructors folder
	##path is the path to where the course directory is to be created
	##courseName is the name of the new course
	def addCourse(path, courseName): #{
		##Create a new directory for the courseName
		newCoursePath = path + courseName
		addFolder(newCoursePath)
		
		courseConfigFile = newCoursePath + "course.config" ##creates the course config file
		
		##create the course config file
		
		
		##if the course config file is not created False is returned to indicate an error
		if courseConfigFile == False: #{ 
			return False
		#}
			
		##creates the course config file and updates the global config
		parent.ConfigParser.addCourse(GLOBAL_PATH, courseName, courseConfigFile)
		
		return True
	#}

	##deletes a course directory in the instructor's directory
	##path is the path to the course directory
	##courseName is the name of the course to be removed
	def deleteCourse(courseName): #{
		path = parent.ConfigParser.get_setting(GLOBAL_PATH, courseName, "course_path")
	
		check = parent.ConfigParser.removeCourse(GLOBAL_PATH, courseName) ##removes the course from the global config file
		
		if check == False: #{
			return False
		#}
		
		deleteFolder(path) ##deletes the course and all assignments under it
		
		return True
	#}
	
	
''' ----------------------------- Section of code that is used for creating and deleting assignments --------------------------------------'''	

	##creates a new assignment directory inside the course directory
	##assignmentName is the name of the new directory
	##path is the path to the course directory, assignmentName is the name of the assignment, dueDate is the day the assignment is dueDate
	##team identifies if the assignment is a team assignment, maxSubmissions are the total number of submissions allowed, lateDays are the 
	##number of days allowed for late submission
	def addAssignment(courseName, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		path = parent.ConfigParser.get_setting(GLOBAL_PATH, courseName, "course_path")
		
		addFolder(path) ##creates a new folder for the assignment
		
		assignmentConfigFile = path + "assignment.config"
		
		##creates the assignment config file
		parent.ConfigParser.addProject(assignmentConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		
		'''
		##gets user group
		#userGroup =

		##creates a folder for each student enrolled in the class
		for elem in userGroup: #{
			newPath = path + elem
			addFolder(newPath)
		#}
		'''
		return True
	#}

	##deletes the assignment specified by assignmentName
	##assignmentName is the assignment to be deleted
	##path is the path to the course directory
	def deleteAssignment(assignmentName, path): #{
		courseConfigFile = path + "course.config"
		
		##removes the assignment from the course config file
		parent.ConfigParser.removeProject(courseConfigFile, assignmentName)
		
		##removes the directory and all subdirectories and files
		deletFolder(path + assignmentName)
		
		return True
	#}

	##modifes the config file of an existing assignment
	##assignmentName is the name of the new directory
	##path is the path to the course directory, assignmentName is the name of the assignment, dueDate is the day the assignment is dueDate
	##team identifies if the assignment is a team assignment, maxSubmissions are the total number of submissions allowed, lateDays are the 
	##number of days allowed for late submission
	def modifyAssignment(path, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		courseConfigFile = path + "course.config"
		
		parent.ConfigParser.modifyProject(courseConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		
		return True
	#}
	
''' ----------------------------------- Section of code that is used for grading -------------------------------------------------------'''	

	##Gives a grade to the student
	##path is the path to the student's directory in an assignment
	##gradeRecieved is the grade recieved for the assignment
	def enterGrade(path, gradeRecieved): #{
		gradeFile = path + "grade.txt"
		
		file grade = open(gradeFile, "w")
		
		grade.write("Grade Recieved: " + gradeRecieved)
		
		grade.close()
	#}
	
''' ----------------------------------- Section of code that is used for creating folders --------------------------------------------------'''	
	#x is the path including the new directory name
	def addFolder(x): #{
		#NOTE!-------------------------------------------------------------------------------------
		# mkdir has another parameter that sets permissions for the new directory
		#!-----------------------------------------------------------------------------------------
		os.mkdir(x); #a new directory is made
	#}

	def deleteFolder(x): #{
		os.rmtree(x) ##removes the directory and all directories and files inside it
	#}
	
'''---------------------------------- Code that is used for testing ------------------------------------------------------------------'''
	##tests the addCourse function
	def testAddCourse() #{
		
	#}
	
	##tests the deleteCourse function
	def testDeleteCourse() #{
		
	#}

	##tests the addAssignment function
	def testAddAssignment() #{
		
	#}

	##tests the deleteAssignment function
	def testDeleteAssignment() #{
		
	#}
	
	##main method
	def main(): #{
		
	#}
	
	
	
	
	
	
	
	
	
	
	