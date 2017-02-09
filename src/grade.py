#Code for grading assignments

class grader:

	def __init__(self): #{
		return
	#}
	
	##Gives a grade to the student
	##path is the path to the student's directory in an assignment
	##gradeRecieved is the grade recieved for the assignment
	def enterGrade(path, gradeRecieved): #{
		gradeFile = path + "grade.txt"
		
		file grade = open(gradeFile, "w")
		
		grade.write("Grade Recieved: " + gradeRecieved)
		
		grade.close()
	#}