#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================
import optparse
import os
from ConfigParser import SafeConfigParser
from distutils.util import strtobool
from pathlib import Path    # needs:  sudo pip install pathlib
from dateutil.parser import parse # needs: sudo pip install python-dateutil
from datetime import datetime



# ConfigManager handles configuration and config files..
class ConfigManager:

	def __init__(self):
		return	

''' Begin API for managing course config file '''
	def addProject(self, courseConfigFile, projectName, dueDate, team, maxSubmissions, lateDays):
		## example : addProject( "testCourse.config", "lab1", "12-05-2017", true, 100, 0)
		## courseConfigFile = os.getcwd() + '/' courseName + ".config"

		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unablle to find "  + courseConfigFile)
			return false

		try:
			dueDate = parse(dueDate)
		except ValueError:
			print("ERROR: incorrect format for dueDate specified \n Setting due date to 2099-12-31")
			dueDate = parse("2099-12-31") ## infinity date in the future

		try:
			teamProj = bool(team)
		except:
			print("ERROR: incorrect format for team specified. Use true/false")
			teamProj = false


		config = get_config(courseConfigFile)
		config.add_section(projectName)
		config.set(projectName, 'team', team)
		config.set(projectName, 'max_submissions', max_submissions)
		config.set(projectName, 'due', str(dueDate) )
		config.set(projectName, 'late days', lateDays )

		
		with open(courseConfigFile, 'wb') as f:
			config.write(f)
		return true

	def removeProject(self, courseConfigFile, projectName):
		## e.g. removeProject("testCourse.config", "lab1" )
		print("removing " + projectName + " from " + courseConfigFile)
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return false

		config = get_config(courseConfigFile)
		config.remove_section(projectName)

		with open(path, "wb") as config_file:
			config.write(config_file)
		return true
	
	def modifyProject(self, courseConfigFile, projectName, dueDate, team, maxSubmissions, lateDays):
		## example : modifyProject( "testCourse.config", "lab2", "12-05-2017", true, 100, 0)
		print("function to modify an existing course")
		removeProject(courseConfigFile,  projectName )
		addProject( courseConfigFile, projectName, dueDate , team, maxSubmissions, lateDays)
		##update_setting(path, section, setting, value)

	def getProjects(self, courseConfigFile):
		config = ConfigParser.RawConfigParser()
		config.read(courseConfigFile)
		return config.sections()


	def getProjectInfo(self, courseConfigFile, projectName):
		config = ConfigParser.RawConfigParser()
		config.read(courseConfigFile)

		for proj in config.sections()
			if proj == projectName
				return config.options(proj)

''' Begin API for managing global config file '''


	def addCourse(self, globalConfigFile, courseName, courseConfigFile):
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return false
		my_file = Path(globalConfigFile)
		if not my_file.is_file():
			print("Unablle to find "  + globalConfigFile)
			return false


		config = get_config(courseConfigFile)
		config.add_section(courseName)
		config.set(courseName, 'course_config_file', courseConfigFile)
		## config.set(courseName, 'contact info: ', contactInfo)

		with open(courseConfigFile, 'wb') as f:
			config.write(f)
		return true

	def removeCourse(self, globalConfigFile, courseName):
		my_file = Path(courseConfigFile)
		if not my_file.is_file():
			print("Unable to find "  + courseConfigFile)
			return false
		config = ConfigParser.RawConfigParser()
		config.read(courseConfigFile)

		config.remove_section(courseName)
		return true


''' Begin ConfigParser API '''
 
	def get_config(self,path):
	    """
	    Returns the config object
	    """
	    if not os.path.exists(path):
	        create_config(path)
	 
	    config = ConfigParser.ConfigParser()
	    config.read(path)
	    return config
	 
	 
	def get_setting(self, path, section, setting):
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
		print("***Testing config generator***")
		cm = ConfigManager();
		

		
if __name__ == '__main__':
    main()
