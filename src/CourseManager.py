import locale
import os
import shutil
import ConfigManager
import configparser
import GradeConfigManager
import grp
import pwd
import stat

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
			print("Course already exists")
			return False
		
		try:
			self.addFolder(newCoursePath)
		except OSError: 
			print("OSError")
			return False
		
		courseConfigFile = newCoursePath + "/course.config" ##creates the course config file
		
		##create the course config file
		try:
			configFile = open(courseConfigFile, "w")
			configFile.close()
		except:
			print("Config creation error")
			return False
		
		##updates the global config
		check = self.manager.addCourse(self.parent.GLOBAL_PATH, courseName, courseConfigFile, newCoursePath, userGroup)
		
		##if the course config file is not created False is returned to indicate an error
		if check == False:
			print("ConfigManager failure")
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
			userGroup = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName,'user_group')
		except configparser.NoSectionError:
			return False
		
		courseConfigFile = path + "/course.config"
		assignmentPath = path + "/" + assignmentName
		
		
		if os.path.exists(assignmentPath):
			#print("Assignment already exists")
			return False
		
		try:
			self.addFolder(assignmentPath) ##creates a new folder for the assignment
		except OSError:
			return False
		
		
		##adds the assignment to the global config file
		check = self.parent.configManager.addProject(courseConfigFile, assignmentName, dueDate, team, maxSubmissions, lateDays)
		
		if not check:
			return False
		
		##Create the student directories
		try:
			group = grp.getgrnam(userGroup)
			for user in group.gr_mem:
				#self.addFolder(assignmentPath + "/smithhe")
				studentFolder = assignmentPath + "/" + user
				self.addStudentFolder(studentFolder, user)
				studentConfig = studentFolder + "/grade.config"
				##create the course config file
				
				try:
					configFile = open(studentConfig, "w")
					configFile.close()
				except:
					return False
		except KeyError:
			return False
		
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

	##modifes the course config file of an existing assignment
	def modifyAssignment(self, courseName, assignmentName, settingName, newValue): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		courseConfigFile = path + "/course.config"
		#assignmentConfigFile = path + "/" + assignmentName + "/assignment.config"
		
		try:
			self.parent.configManager.update_setting(courseConfigFile, assignmentName, settingName, newValue)
		except configparser.NoSectionError:
			return False
		
		return True
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	##  Section of code that is used for grading
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##Creates the grade config file and enteres in the grade content for the student
	def enterGrade(self, courseName, assignmentName, studentName, gradeRecieved, bonus, feedback): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			print("Config Error")
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		##create the grade config file
		try:
			gradeConfigFile = open(gradeConfigPath, "w")
			gradeConfigFile.close()
		except:
			print("Error with creating grade config")
			#print(gradeConfigPath)
			return False
		
		try:
			check = self.parent.gradeManager.addGrade(gradeConfigPath, gradeRecieved, bonus, feedback)
		except:
			print("Grade Config Error")
			return False
		
		return check
	#}
	
	##Returns in string format the grade recieved
	def getGrade(self, courseName, assignmentName, studentName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			gradeRecieved = self.parent.gradeManager.getGrade(gradeConfigPath)
			return gradeRecieved
		except configparser.NoSectionError:
			return False
	#}
	
	##Returns in string format the amount of bonus points recieved
	def getBonus(self, courseName, assignmentName, studentName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			bonusRecieved = self.parent.gradeManager.getBonus(gradeConfigPath)
		except configparser.NoSectionError:
			return False
		
		return bonusRecieved
	#}
	
	##Returns the feedback recieved
	def getFeedback(self, courseName, assignmentName, studentName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			feedbackRecieved = self.parent.gradeManager.getFeedback(gradeConfigPath)
		except configparser.NoSectionError:
			return False
		
		return feedbackRecieved
	#}
	
	##Edits the grade for the student, returns false if student's folder doesn't exist or if failure occurs
	def editGrade(self, courseName, assignmentName, studentName, newGrade): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			self.parent.gradeManager.editGrade(gradeConfigPath, newGrade)
		except configparser.NoSectionError:
			return False
		
		return True
	#}
	
	##Edits the bonus points recieved by the student, returns false is student doesn't exist or is failure occurs
	def editBonus(self, courseName, assignmentName, studentName, newBonus): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			self.parent.gradeManager.editBonus(gradeConfigPath, newBonus)
		except configparser.NoSectionError:
			return False
		
		return True
	#}
	
	def editFeedback(self, courseName, assignmentName, studentName, newFeedback): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
		
		gradeConfigPath = path + "/" + assignmentName + "/" + studentName + "/grade.config"
		
		try:
			self.parent.gradeManager.editFeedback(gradeConfigPath, newFeedback)
		except configparser.NoSectionError:
			return False
		
		return True
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code that is used for creating folders
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	def addFolder(self, x): #{
		os.mkdir(x) ##a new directory is made
	#}
	
	def addStudentFolder(self, x, student): #{
		collection = pwd.getpwnam(student)
		studentID = collection.pw_uid
		instructorGroup = self.parent.configManager.getInstructorGroup(self.parent.GLOBAL_PATH)
		groupInfo = grp.getgrnam(instructorGroup)
		instructorID = groupInfo.gr_gid
		os.mkdir(x)
		#os.chown(x, studentID, instructorID)
		os.chmod(x, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
	#}

	##removes the directory and all directories and files inside it
	def deleteFolder(self, x): #{
		shutil.rmtree(x) 
	#}
	
	##-------------------------------------------------------------------------------------------------------------------------------------
	## Section of code for GUI Functionalilty
	##-------------------------------------------------------------------------------------------------------------------------------------
	
	##returns the path to the course directory if it exists
	##returns false otherwise
	def courseNameToPath(self, courseName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
		except configparser.NoSectionError:
			return False
			
		return path
	#}
	
	##Names of different assignment config settings are: "team", "max_submissions", "due", and "late days"
	##!!Note!! The name of the setting must be exactly one of the above or False will be returned
	def getAssignmentSetting(self, courseName, assignmentName, settingName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
			courseConfigFile = path + "/course.config"
			value = self.parent.configManager.get_setting(courseConfigFile, assignmentName, settingName)
		except configparser.NoSectionError:
			return False
		
		return value
	#}
	
	##returns an array of courses
	def getCourseList(self): #{
		return self.parent.configManager.getCourseList(self.parent.GLOBAL_PATH) 
	#}

	##returns an array of assignments for a course
	def getAssignmentList(self, courseName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
			courseConfigFile = path + "/course.config"
		except configparser.NoSectionError:
			return False
			
		return self.parent.configManager.getProjects(courseConfigFile)
	#}

	##returns the name of the user group for a course
	def getCourseUserGroup(self, courseName): #{
		try:
			path = self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "course_path")
			courseConfigFile = path + "/course.config"
		except configparser.NoSectionError:
			return False
			
		return self.parent.configManager.get_setting(self.parent.GLOBAL_PATH, courseName, "user_group")
	#}



