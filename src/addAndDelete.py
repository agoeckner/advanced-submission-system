import locale

class addAndDelete:
	parent = None

	#constructor
	def __init__(self, parent): #{
		self.parent = parent
	#}
	
	#creates a new course directory in the instructors folder
	#courseName is the name for the new directory
	#instructor is the instructor's username which is used to find their personal directory
	def addCourse(courseName, path): #{
		
		#Create a new directory for the courseName
		newCoursePath = path + courseName
		addFolder(newCoursePath)
		
		courseConfigFile = newCoursePath + "course.config" #creates the course config file
		#creates the course config file and updates the global config
		parent.ConfigParser.addCourse(GLOBAL_PATH, courseName, courseConfigFile)
	#}

	#deletes a course directory in the instructor's directory
	#courseName is the name of the directory to be deleted
	#instructor is the instructor's username which is used to find their personal directory
	def deleteCourse(courseName): #{
		parent.ConfigParser.removeCourse(GLOBAL_PATH, courseName) #removes the course from the global config file
		
		deleteFolder(path) #deletes the course and all assignments under it
	#}

	#creates a new assignment directory inside the course directory
	#assignmentName is the name of the new directory
	#courseName is the directory under which the new directory is to be made
	#configParameters are the arguments to be put in the assignments local config file
	def addAssignment(): #{
		
		
	#}

	#deletes the assignment specified by assignmentName
	#assignmentName is the assignment to be deleted
	#courseName is the name of the course the assignment is in
	def deleteAssignment(assignmentName, instructor, courseName): #{
		#Get the instructors directory path from the config file
		instructorsPath = getInstructorPath(instructor)
		
		
	#}

	#Creates the config file for an assignment
	#path is the path to the course directory
	#dueDate is the day the assignment is dueDate, team identifies if it is a team assignment, maxSubmissions is the maximum number of submissions allowed
	#lateDays are the number of days allowed for late submissions
	def createAssignmentConfig(path, assignmentName, dueDate, team, maxSubmissions, lateDays): #{
		
	#}

	#opens the global config file and returns the path to the instructor's directory
	def getInstructorPath(instructor): #{
		encoding = locale.getpreferredencoding() #gets the users prefered character encoding
		
		file = open("/etc/submission/global.config", encoding); #opens the global config file
		
		#Get instructors path from the global config file
		for line_of_text in f: #{
			if line_of_text.find(instructor) != -1: #{
				instructorsPath = line_of_text
			#}
		#}
		
		return instructorsPath
	#}