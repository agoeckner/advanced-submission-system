import locale

class addAndDelete:
	parent = None
	
	##to get a section for a course
	get_setting(GLOBAL_PATH, courseName, "course_path")
	
	
	
	##TODO: check for existing courses or assignments when creating or deleting
	##TODO: check that the config files are being created after calling configmanager
	
	##constructor
	def __init__(self, parent): #{
		self.parent = parent
	#}
	
	##creates a new course directory in the instructors folder
	##path is the path to where the course directory is to be created
	##courseName is the name of the new course
	def addCourse(path, courseName): #{
		##Create a new directory for the courseName
		newCoursePath = path + courseName
		addFolder(newCoursePath)
		
		courseConfigFile = newCoursePath + "course.config" ##creates the course config file
		if courseConfigFile == False: #{
			
		#}
			
		##creates the course config file and updates the global config
		parent.ConfigParser.addCourse(GLOBAL_PATH, courseName, courseConfigFile)
		
		return True
	#}

	##deletes a course directory in the instructor's directory
	##path is the path to the course directory
	##courseName is the name of the course to be removed
	def deleteCourse(path, courseName): #{
		parent.ConfigParser.removeCourse(GLOBAL_PATH, courseName) ##removes the course from the global config file
		
		deleteFolder(path) ##deletes the course and all assignments under it
		
		return True
	#}

	##creates a new assignment directory inside the course directory
	##assignmentName is the name of the new directory
	##path is the path to the course directory, assignmentName is the name of the assignment, dueDate is the day the assignment is dueDate
	##team identifies if the assignment is a team assignment, maxSubmissions are the total number of submissions allowed, lateDays are the 
	##number of days allowed for late submission
	def addAssignment(path, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	