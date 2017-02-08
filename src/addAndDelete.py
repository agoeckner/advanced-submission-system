import locale

class addAndDelete:
	parent = None

	##constructor
	def __init__(self, parent): #{
		self.parent = parent
	#}
	
	##creates a new course directory in the instructors folder
	##courseName is the name for the new directory
	##instructor is the instructor's username which is used to find their personal directory
	def addCourse(courseName, path): #{
		
		##Create a new directory for the courseName
		newCoursePath = path + courseName
		addFolder(newCoursePath)
		
		courseConfigFile = newCoursePath + "course.config" ##creates the course config file
		
		##creates the course config file and updates the global config
		parent.ConfigParser.addCourse(GLOBAL_PATH, courseName, courseConfigFile)
	#}

	##deletes a course directory in the instructor's directory
	##courseName is the name of the directory to be deleted
	##instructor is the instructor's username which is used to find their personal directory
	def deleteCourse(courseName): #{
		parent.ConfigParser.removeCourse(GLOBAL_PATH, courseName) ##removes the course from the global config file
		
		deleteFolder(path) ##deletes the course and all assignments under it
	#}

	##creates a new assignment directory inside the course directory
	##assignmentName is the name of the new directory
	##courseName is the directory under which the new directory is to be made
	##configParameters are the arguments to be put in the assignments local config file
	def addAssignment(courseName, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		manager = parent.ConfigParser.get_config(GLOBAL_PATH)
		
		##get path to the specfic course
		#path = manager.getCoursePath
		
		addFolder(path) ##creates a new folder for the assignment
		
		assignmentConfigFile = path + "assignment.config"
		##creates the assignment config file
		parent.ConfigParser.addProject(assignmentConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		
		##gets user group
		#userGroup =

		"""
		##creates a folder for each student enrolled in the class
		for elem in userGroup: #{
			newPath = path + elem
			addFolder(newPath)
		#}
		"""
	#}

	##deletes the assignment specified by assignmentName
	##assignmentName is the assignment to be deleted
	##courseName is the name of the course the assignment is in
	def deleteAssignment(assignmentName, instructor, courseName): #{
		
		
	#}
