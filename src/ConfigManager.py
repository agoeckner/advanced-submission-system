#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================
import optparse
import os
import ConfigParser
from distutils.util import strtobool
from pathlib import Path    # needs:  sudo pip install pathlib
from dateutil.parser import parse # needs: sudo pip install python-dateutil
from datetime import datetime



# ConfigManager handles configuration and config files..
# class ConfigManager:

# def __init__():
# 	return	

''' 
Begin API for managing course config file 
'''
def addProject( courseConfigFile, projectName, dueDate, team, maxSubmissions,lateDays):
	## example : addProject( "testCourse.config", "lab1", "12-05-2017", True, 100, 0)
	## courseConfigFile = os.getcwd() + '/' courseName + ".config"
	my_file = Path(courseConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + courseConfigFile)
		return false

	try:
		dueDate = parse(dueDate)
	except ValueError:
		print("ERROR: incorrect format for dueDate specified \n Setting due date to 2099-12-31")
		dueDate = parse("2099-12-31") ## infinity date in the future

	try:
		teamProj = bool(team)
	except:
		print("ERROR: incorrect format for team specified. Use True/false")
		teamProj = false

	config = ConfigParser.ConfigParser() # get_config(courseConfigFile)
	config.read(courseConfigFile)

	# print ("config : " + repr(config) )
	try:
		config.add_section(projectName)
		config.set(projectName, 'team', team)
		config.set(projectName, 'max_submissions', maxSubmissions)
		config.set(projectName, 'due', str(dueDate) )
		config.set(projectName, 'late days', lateDays )
	except ConfigParser.DuplicateSectionError :
		print("\t[-] "  + projectName + " already exists")
	
	with open(courseConfigFile, 'wb') as f:
		config.write(f)
	return True

def removeProject( courseConfigFile, projectName):
	## e.g. removeProject("testCourse.config", "lab1" )
	# print("removing " + projectName + " from " + courseConfigFile)
	my_file = Path(courseConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + courseConfigFile)
		return false

	config = ConfigParser.ConfigParser() # get_config(courseConfigFile)
	config.read(courseConfigFile)
	config.remove_section(projectName)

	with open(courseConfigFile, "wb") as config_file:
		config.write(config_file)
	return True

def modifyProject( courseConfigFile, projectName, dueDate, team, maxSubmissions, lateDays):
	## example : modifyProject( "testCourse.config", "lab2", "12-05-2017", True, 100, 0)
	# print("function to modify an existing course")
	removeProject(courseConfigFile,  projectName )
	addProject( courseConfigFile, projectName, dueDate , team, maxSubmissions, lateDays)
	##update_setting(path, section, setting, value)

def getProjects( courseConfigFile):
	config = ConfigParser.RawConfigParser()
	config.read(courseConfigFile)
	return config.sections()


def getProjectInfo( courseConfigFile, projectName):
	config = ConfigParser.RawConfigParser()
	config.read(courseConfigFile)
	conf_sections = config.sections()
	for proj in conf_sections :
		if proj == projectName:
			return config.options(proj)


'''
Begin API for managing global config file
'''

def addCourse( globalConfigFile, courseName, courseConfigFile, coursePath):
	my_file = Path(courseConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + courseConfigFile)
		return false
	my_file = Path(globalConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + globalConfigFile)
		return false


	config = ConfigParser.ConfigParser() # get_config(courseConfigFile)
	config.read(globalConfigFile)

	try:
		config.add_section(courseName)
	except ConfigParser.DuplicateSectionError :
		print("\t[-] "  + courseName + " already exists")
	config.set(courseName, 'course_config_file', courseConfigFile)
	config.set(courseName, 'course_path', coursePath)
	## config.set(courseName, 'contact info: ', contactInfo)

	with open(courseConfigFile, 'wb') as f:
		config.write(f)
	return True

def removeCourse( globalConfigFile, courseName):
	my_file = Path(courseConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + courseConfigFile)
		return False

	my_file = Path(globalConfigFile)
	if not my_file.is_file():
		print("Unable to find "  + globalConfigFile)
		return False	

	config = ConfigParser.RawConfigParser()
	config.read(courseConfigFile)

	config.remove_section(courseName)
	return True

def getCourseList(GLOBAL_PATH): 
	my_file = Path(GLOBAL_PATH)
	if not my_file.is_file():
		print("Unable to find "  + GLOBAL_PATH)
		return false
	config = ConfigParser.RawConfigParser()
	config.read(GLOBAL_PATH)
	
	return config.sections()

''' 
Begin API for ConfigParser API
'''

def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    print "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value)
    return value
 

def update_setting(path, section, setting, value):
	"""
	Update a setting
	"""
	config = get_config(path)
	config.set(section, setting, value)
	with open(path, "wb") as config_file:
		config.write(config_file)
 
 
def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "wb") as config_file:
        config.write(config_file)

def main():
	print("***Testing course config API***")
	courseConfig = 'testCourse.config'
	globalConfig = 'testGlobal.config'
	
	print("[+] Adding lab2 to course config file")
	if addProject( courseConfig, 'lab2', '12-04-2016', True, 15, 5) :
		print("[+] project added")
	print("[+] Adding lab3 to course config file")
	if addProject( courseConfig, 'lab3', '12-05-2016', True, 25, 0) :
		print("[+] project added")

	print("[+] Adding project1 to course config file")
	if addProject( courseConfig, 'project1', '12-08-2016', False, 5, 5) :
		print("[+] project added")
	
	print("[+] removing lab2")
	if removeProject(courseConfig, 'lab2') :
		print("[+] project removed")

	print("Printing courses in " + courseConfig)
	course_list = getProjects(courseConfig)
	print("[")
	for course in course_list:
		print(course)
	print(" ]")

	print("=======")
	print("***Testing global config API***")
	


if __name__ == '__main__':
    main()

