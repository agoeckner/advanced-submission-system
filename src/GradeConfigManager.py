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
class GradeConfigManager:

	def __init__(self):
		return	
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
	'''
	Begin grade config management API
	'''

	def addGrade(self, grade_config_path, grade, bonus, feedback):
		'''
		Adds the grade info to an existing grade file
		'''
		config = self.get_config(grade_config_path)
		sec_name = "gradeInfo"
		try:
			config.add_section(sec_name)
			config.set(sec_name, 'Grade', str(grade) )
			config.set(sec_name, 'Bonus', str(bonus) )
			config.set(sec_name, 'Comments', str(feedback) )

		except configparser.DuplicateSectionError :
			print("\t[-] grade already added")
			return False
		
		with open(grade_config_path, 'w') as f:
			config.write(f)
		return True

	def getGrade(self, grade_config_path):
		return self.get_setting(grade_config_path, "gradeInfo", "Grade")

	def getBonus(self, grade_config_path):
		return self.get_setting(grade_config_path, "gradeInfo", "Bonus")

	def getFeedback(self, grade_config_path):
		return self.get_setting(grade_config_path, "gradeInfo", "Comments")


	def editGrade(self, grade_config_path, new_grade):
		self.update_setting(grade_config_path, "gradeInfo", "Grade", new_grade)

	def editBonus(self, grade_config_path, new_grade):
		self.update_setting(grade_config_path, "gradeInfo", "Bonus", new_grade)

	def editFeedback(self, grade_config_path, new_feedback):
		self.update_setting(grade_config_path, "gradeInfo", "Comments", new_feedback)

	def getCourseGrades(self, project_path):
		rootdir = project_path #"~/cs408/advanced-submission-system/test/testCourse/testProject"
		gradesDict = {}
		if not os.path.isdir(project_path):
			print("[-] invalid path passed in getCourseGrades (path passed: " + project_path + ")")
			return None

		for subdir, dirs, files in os.walk(rootdir):
			for studentDir in dirs:
				gradeConfigFile = os.path.join(subdir, studentDir)
				gradeConfigFile += "/Grade.config"
				my_file = Path(gradeConfigFile)
				if not my_file.is_file():
					print("\t[-] Unable to find grade config file for student : " + studentDir)
					return None
				total_points = "Score: " + str(self.getGrade(gradeConfigFile) ) + " Bonus: " + str( self.getBonus(gradeConfigFile) )
				gradesDict[studentDir] = total_points
		return gradesDict

def main():
	gcm = GradeConfigManager()
	


if __name__ == '__main__':
	main()


