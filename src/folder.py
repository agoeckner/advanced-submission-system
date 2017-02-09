import os
import shuttil

class folder:
	parent = None
	
	#constructor
	def __init__(self, parent): #{
		self.parent = parent
	#}
	
	#x is the path including the new directory name
	def addFolder(x) #{
		#NOTE!-------------------------------------------------------------------------------------
		# mkdir has another parameter that sets permissions for the new directory
		#!-----------------------------------------------------------------------------------------
		os.mkdir(x); #a new directory is made
	#}

	def deleteFolder(x) #{
		os.rmtree(x) #removes the directory and all directories and files inside it
	#}