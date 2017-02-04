#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================
import optparse
import os
from ConfigParser import SafeConfigParser
from distutils.util import strtobool
from pathlib import Path



# ConfigManager handles configuration and config files..
class ConfigManager:

	def __init__(self):
		globalConfigPath = "as_config.config"

	def main():
		print("test config generator")
		write();
		read("aaa");
		remove("aaa");
		modify("aaa");


	def createCourse(courseName, projectName, dueDate, team):
	## write( courseName, bool team, ...,)
	## could also use class object and pass to write
	fileName = courseName + projectName + ".config"
	my_file = Path()
	if my_file.is_file():
		return false
	print("creating course")

	config = SafeConfigParser()
	config.add_section(courseName + '-'+ projectName)
	config.set('course01', 'team', 'yes')
	config.set('course01', 'max_submissions', '5')
	config.set('course01', 'due', '02/12/2017')
	with open('config.ini', 'a') as f:
		config.write(f)

	def remove(courseName):
		print("function to remove a course from system")
	
	def modify(courseName):
		#modify(name, [new args]  OR object)
		print("function to modify an existing course")

	def create_config(path):
    """
    Create a config file
    """
    config = ConfigParser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "font", "Courier")
    config.set("Settings", "font_size", "10")
    config.set("Settings", "font_style", "Normal")
    config.set("Settings", "font_info",
               "You are using %(font)s at %(font_size)s pt")
 
    with open(path, "wb") as config_file:
        config.write(config_file)
 
 
	def get_config(path):
	    """
	    Returns the config object
	    """
	    if not os.path.exists(path):
	        create_config(path)
	 
	    config = ConfigParser.ConfigParser()
	    config.read(path)
	    return config
	 
	 
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
		
if __name__ == '__main__':
    main()




	