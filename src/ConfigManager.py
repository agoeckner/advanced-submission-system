#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================
import optparse
import os
import configparser
from distutils.util import strtobool
from pathlib import Path    # needs:  sudo pip install pathlib
from dateutil.parser import parse # needs: sudo pip install python-dateutil
from datetime import datetime



# ConfigManager handles configuration and config files..
class ConfigManager:

	def __init__(self):
		return	

	''' 
	Begin API for managing course config file 
	'''
	def addProject(self, courseConfigFile, projectName, dueDate, team, maxSubmissions,lateDays):
		## example : addProject( "testCourse.config", "lab1", "12-05-2017", True, 100, 0)
		## courseConfigFile = os.getcwd() + '/' courseName + ".config"
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return False

		try:
			dueDate = parse(dueDate)
		except ValueError:
			print("ERROR: incorrect format for dueDate specified \n Use format mm-dd-yyyy")
			return False
			##dueDate = parse("2099-12-31") ## infinity date in the future
		now = datetime.now()
		if(now > dueDate):
			print("[-] Invalid date specified. Set due date to future date")
			return False

		try:
			teamProj = bool(team)
		except:
			print("ERROR: incorrect format for team specified. Use True/false")
			return False

		config = configparser.ConfigParser() # get_config(courseConfigFile)
		config.read(courseConfigFile)

		# print ("config : " + repr(config) ) ## checks if config is a null object
		try:
			config.add_section(projectName)
			config.set(projectName, 'team', str(team) )
			config.set(projectName, 'max_submissions', str(maxSubmissions) )
			config.set(projectName, 'due', str(dueDate) )
			config.set(projectName, 'late_days', str(lateDays)  )
		except configparser.DuplicateSectionError :
			print("\t[-] "  + projectName + " already exists")
			return False
		
		with open(courseConfigFile, 'w') as f:
			config.write(f)
		return True

	def removeProject( self, courseConfigFile, projectName):
		## e.g. removeProject("testCourse.config", "lab1" )
		# print("removing " + projectName + " from " + courseConfigFile)
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return False

		config = configparser.ConfigParser() # get_config(courseConfigFile)
		config.read(courseConfigFile)
		config.remove_section(projectName)

		with open(courseConfigFile, "w") as config_file:
			config.write(config_file)
		return True

	def modifyProject(self, courseConfigFile, projectName, dueDate, team, maxSubmissions, lateDays):
		## example : modifyProject( "testCourse.config", "lab2", "12-05-2017", True, 100, 0)
		# print("function to modify an existing course")
		self.removeProject(courseConfigFile,  projectName )
		self.addProject( courseConfigFile, projectName, dueDate , team, maxSubmissions, lateDays)
		##update_setting(path, section, setting, value)

	def getProjects(self, courseConfigFile):
		config = configparser.RawConfigParser()
		config.read(courseConfigFile)
		return config.sections()


	def getProjectInfo( self,courseConfigFile, projectName, key):
		config = configparser.RawConfigParser()
		config.read(courseConfigFile)
		conf_sections = config.sections()
		for proj in conf_sections :
			if proj == projectName:
				return config[projectName][key]
		raise Exception("Project not found!")


	'''
	Begin API for managing global config file
	'''

	def addCourse(self, globalConfigFile, courseName, courseConfigFile, coursePath, userGroup):
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return False
		my_file = Path(globalConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + globalConfigFile)
			return False


		config = configparser.ConfigParser() # get_config(courseConfigFile)
		config.read(globalConfigFile)

		try:
			config.add_section(courseName)
		except configparser.DuplicateSectionError :
			print("\t[-] "  + courseName + " already exists")
			return False
		config.set(courseName, 'course_config_file', courseConfigFile)
		config.set(courseName, 'course_path', coursePath)
		config.set(courseName, 'usergroup', userGroup)
		## config.set(courseName, 'contact info: ', contactInfo)

		with open(globalConfigFile, 'w+') as f:
			config.write(f)
		return True

	def removeCourse(self, courseConfigFile, globalConfigFile, courseName):
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return False

		my_file = Path(globalConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + globalConfigFile)
			return False	

		config = configparser.RawConfigParser()
		config.read(globalConfigFile)

		try:
			config.remove_section(courseName)
		except configparser.NoSectionError:
			print("[-] course not present in globalConfigFile")
			return False
		return True
	def addInstructor(self, globalConfigFile, groupName):
		my_file = Path(globalConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + globalConfigFile)
			return False
		config = configparser.ConfigParser() # get_config(courseConfigFile)
		config.read(globalConfigFile)
		try:
			config.add_section('Instructors')
		except configparser.DuplicateSectionError :
			print("\t[-] Instructor section already exists. Use update_setting")
			return False
		config.set('Instructors', 'user_group', groupName)
		
		with open(globalConfigFile, 'r+') as f:
			config.write(f)
		return True
		
	def getInstructorGroup(self, globalConfigFile):
		return self.get_setting(globalConfigFile, 'Instructors', 'user_group')

	def getCourseList(self, globalConfigFile): 
		my_file = Path(globalConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + globalConfigFile)
			return {}
		config = configparser.RawConfigParser()
		config.read(globalConfigFile)
		courses = config.sections()
		try:
			courses.remove('Instructors');
		except ValueError:
			print("[-] Instructors section not in global config file")
		return courses


	''' 
	Begin API for configparser API
	'''
	def get_config(self, path):
		my_file = Path(path)
		if not my_file.is_file():
			print("\t[-] Unable to find "  + path + " in get_config")
			return False
		config = configparser.RawConfigParser()
		config.read(path)
		if not config:
			print("\t[-] Unable to create config object in get_config")
			return False
		return config	    

	def get_setting(self, path, section, setting):
		# method will throw exceptions if section doesn't exist

		config = self.get_config(path)
		if (not config):
			print("[-] get_config failed in get_setting")
			return False
		value = config.get(section, setting)
		#print "{section} {setting} is {value}".format(
		#    section=section, setting=setting, value=value)
		return value	 

	def update_setting(self, path, section, setting, value):
		"""
		Update a setting
		"""
		# method will throw exceptions if section doesn't exist
		config = self.get_config(path)
		if (not config):
			return False
		config.set(section, setting, value)
		with open(path, "w") as config_file:
			config.write(config_file)
		return True	 
	 
	def delete_setting(self, path, section, setting):
		"""
		Delete a setting
		"""
		# method will throw exceptions if section doesn't exist
		config = self.get_config(path)
		if (not config):
			return False
		config.remove_option(section, setting)
		with open(path, "w") as config_file:
			config.write(config_file)
		return True	

def main():
	print("***Testing course config API***")
	courseConfig = '../test/testCourse/testCourse.config'
	globalConfig = '../test/testGlobal.config'
	cm = ConfigManager()
	
	print("[+] Adding lab2 to course config file")
	if cm.addProject( courseConfig, 'lab2', '12-04-2018', True, 15, 5) :
		print("[+] project added")
	print("[+] Adding lab3 to course config file")
	if cm.addProject( courseConfig, 'lab3', '12-05-2018', True, 25, 0) :
		print("[+] project added")

	print("[+] Adding project1 to course config file")
	if cm.addProject( courseConfig, 'project1', '12-08-2018', False, 5, 5) :
		print("[+] project added")
	
	print("[+] removing lab2")
	if cm.removeProject(courseConfig, 'lab2') :
		print("[+] project removed")

	print("Printing courses in " + courseConfig)
	proj_list = cm.getProjects(courseConfig)
	print("[")
	for proj in proj_list:
		print(proj)
	print(" ]")
	print("[+] Changing due date for project1")
	cm.modifyProject(courseConfig, 'project1', '12-15-2018', False, 5, 5)

	print("Printing courses in " + courseConfig)
	proj_list = cm.getProjects(courseConfig)
	print("[")
	for proj in proj_list:
		print(proj)
	print(" ]")

	print("=======")
	print("***Testing global config API***")

	print("[+] adding 4 course")
	if not cm.addCourse( globalConfig, "cs240", courseConfig, "some/path/to/course/dir", "cs240students"):
		print("[-] unable to add cs240")
	if not cm.addCourse( globalConfig, "cs241", courseConfig, "some/path/to/course/dir1", "cs241students"):
		print("[-] unable to add cs241")
	if not cm.addCourse( globalConfig, "cs242", courseConfig, "some/path/to/course/dir2", "cs242students"):
		print("[-] unable to add cs242")
	if not cm.addCourse( globalConfig, "cs243", courseConfig, "some/path/to/course/dir3", "cs243students"):
		print("[-] unable to add cs243")

	print("[+] Course List: ")
	course_list = cm.getCourseList(globalConfig)
	print("[")
	for course in course_list:
		print(course)
	print(" ]")

	print("[+] removing cs242 from global config file")
	if not cm.removeCourse( courseConfig, globalConfig, "cs242"):
		print("[-] Unable to remove cs242 from global config")

	print("[+] Course List: ")
	course_list = cm.getCourseList(globalConfig)
	print("[")
	for course in course_list:
		print(course)
	print(" ]")

if __name__ == '__main__':
    main()

