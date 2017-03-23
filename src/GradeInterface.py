#=================================
# Advanced Submission System
# CS 40800 - Software EngineerGing
# Purdue University
#=================================

import curses
import grp
import time
import ProgramException
import ui.Button as Button
import ui.InputManager as InputManager
import ui.Picker as Picker
import ui.TextEditField as TextEditField

PROGRAM_TITLE = "ADVANCED SUBMISSION SYSTEM"
PROGRAM_SUBTITLE = "Purdue Computer Science"
INTERFACE_TITLE = "GRADES"

TERMINAL_MIN_Y = 24
TERMINAL_MIN_X = 80

MODE_STUDENT = 0
MODE_INSTRUCTOR = 1

# GradeInterface is used to submit assignments.
class GradeInterface:
	def __init__(self, parent, mode):
		self.parent = parent
		self.mode = mode
		self.inputManager = InputManager.InputManager(self)
		self.run = True
		self.course = ""
		self.assignment = ""
		self.student = ""
		self.lastMsgLen = 0
	
	def show(self):
		try:
			curses.wrapper(self._draw)
			self.onExit()
		except KeyboardInterrupt:
			raise
		except Exception as err:
			print("curseserror: " + str(err))
			raise
	
	def onExit(self):
		# Shutdown message.
		print("Goodbye!")
	
	def _draw(self, stdscr):
		self.screenMain = stdscr
		try:
			# UI Setup
			curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
			curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
			curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
			self.screenSize = stdscr.getmaxyx()
			# Check if size below 24x80.
			if self.screenSize[0] < TERMINAL_MIN_Y or self.screenSize[1] < TERMINAL_MIN_X:
				raise Exception("Terminal too small! Minimum size 24x80.")
			curses.curs_set(0)
			stdscr.bkgd(curses.color_pair(0))
			stdscr.nodelay(1)
			stdscr.refresh()
			
			# Top panel.
			self.panelTop = stdscr.derwin(2, self.screenSize[1], 0, 0)
			self.panelTop.bkgd(curses.color_pair(2))
			
			# Information panel on the left of the top panel.
			self.panelInfo = self.panelTop.derwin(2, self.screenSize[1] - 12, 0, 0)
			self.panelInfo.addstr(0, 0, PROGRAM_TITLE, curses.A_STANDOUT)
			self.panelInfo.addstr(1, 3, PROGRAM_SUBTITLE, curses.A_NORMAL)
			titlePosX = int((self.screenSize[1] - len(PROGRAM_TITLE) - 12 -
				len(INTERFACE_TITLE)) / 2) + len(PROGRAM_TITLE)
			self.panelInfo.addstr(1, titlePosX, INTERFACE_TITLE, curses.A_NORMAL)
			self.panelInfo.refresh()
			
			# Time panel in the top-right corner.
			self.panelTime = self.panelTop.derwin(2, 12, 0, self.screenSize[1] - 12)
			self.panelTime.addstr(0, 0, "Current Time", curses.A_UNDERLINE)
			
			# Main panel.
			self.panelMain = stdscr.derwin(self.screenSize[0] - 4, self.screenSize[1] - 2, 3, 1)
			self.panelMain.bkgd(curses.color_pair(1))
			self.panelMain.addstr(
				self.screenSize[0] - 5,
				self.screenSize[1] - 36,
				"Tip: Use the spacebar to select.",
				curses.A_DIM)
			# self.panelMain.box()
			self.panelMain.refresh()
			
			# Course picker.
			pickCourseSizeY = int((self.screenSize[0] - 4) / 3)
			self.pickCourse = Picker.Picker(
				parent = self.panelMain,
				positionYX = (1, 1),
				sizeYX = (pickCourseSizeY, int((self.screenSize[1] - 4) / 3)),
				title = 'Course',
				options = self.parent.courseManager.getCourseList(),
				footer = "",
				maxSelect = 1,
				c_empty = "( )",
				c_selected = "(X)")
			self.pickCourse.redraw()
			self.pickCourse.setCallback(self.onSelectCourse)
			self.inputManager.addElement(self.pickCourse)
			
			# Assignment picker.
			self.pickAssignment = Picker.Picker(
				parent = self.panelMain,
				positionYX = (pickCourseSizeY + 1, 1),
				sizeYX = (self.screenSize[0] - 6 - pickCourseSizeY,
					int((self.screenSize[1] - 4) / 3)),
				title = 'Assignment',
				options = [],
				footer = "",
				maxSelect = 1,
				c_empty = "( )",
				c_selected = "(X)")
			self.pickAssignment.redraw()
			self.pickAssignment.setCallback(self.onSelectAssignment)
			self.pickAssignmentVisible = False
			
			if self.mode is MODE_STUDENT:
				self._drawStudent()
				self.displayMessage("Running in STUDENT mode.")
			elif self.mode is MODE_INSTRUCTOR:
				self._drawInstructor()
				self.displayMessage("Running in INSTRUCTOR mode.")

			# UI Loop
			while self.run:
				self._drawUpdate()
				# No need to refresh faster than 1 FPS for this example...
				time.sleep(0.01)
		except Exception as err:
			raise err

	def _drawInstructor(self):
		try:
			# Assignment edit panel.
			editPanelPosYX = (self.screenSize[0] - 12, int((self.screenSize[1] - 4) / 3) + 1)
			editPanelSizeYX = (7, 2 * int((self.screenSize[1] - 3) / 3))
			self.editPanel = self.panelMain.derwin(
				editPanelSizeYX[0], editPanelSizeYX[1], # size
				editPanelPosYX[0], editPanelPosYX[1]) # position
			self.editPanel.bkgd(curses.color_pair(1))
			centerTip = "Assignment options are changed here."
			self.editPanel.addstr(
				int(editPanelSizeYX[0] / 2),
				int(editPanelSizeYX[1] / 2) - int(len(centerTip) / 2),
				centerTip,
				curses.A_DIM)
			self.editPanel.box()
			self.editPanel.refresh()
			
			# Create edit panels, which are hidden for now.
			self._createAssignmentNewPanel(editPanelSizeYX, editPanelPosYX)
			self._createGradeEditPanel(editPanelSizeYX, editPanelPosYX)
			
			# Student intro. panel.
			studentPanelPosYX = (1, int((self.screenSize[1] - 4) / 3) + 1)
			self.studentPanelSizeYX = (self.screenSize[0] - 6 - editPanelSizeYX[0], 2 * int((self.screenSize[1] - 3) / 3))
			self.studentPanel = self.panelMain.derwin(
				self.studentPanelSizeYX[0], self.studentPanelSizeYX[1], # size
				studentPanelPosYX[0], studentPanelPosYX[1]) # position
			self.studentPanel.bkgd(curses.color_pair(1))
			centerTip = "Please select a course to view grades."
			self.studentPanel.addstr(
				int(self.studentPanelSizeYX[0] / 2),
				int(self.studentPanelSizeYX[1] / 2) - int(len(centerTip) / 2),
				centerTip,
				curses.A_DIM)
			self.studentPanel.box()
			self.studentPanel.refresh()
			
			# Student list panel.
			self.pickStudent = Picker.Picker(
				parent = self.panelMain,
				positionYX = studentPanelPosYX,
				sizeYX = self.studentPanelSizeYX,
				title = 'Students    ...    Grade',
				options = [],
				footer = "",
				maxSelect = 1,
				c_empty = "",
				c_selected = "")
			self.pickStudent.setCallback(self.onSelectStudent)
			self.pickStudentVisible = False
			
		except Exception as err:
			raise err

	def _createAssignmentNewPanel(self, size, pos):
		self.editAssignmentVisible = False
		##Edit assignment name
		self.assignmentNameLabel = "Assignment name:"
		self.assignmentNamePos = (1, 2)
		self.editAssignmentName = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 23,
			sizeYX = (1, 29),
			positionYX = (self.assignmentNamePos[0], self.assignmentNamePos[1] + len(self.assignmentNameLabel) + 1))
		self.editAssignmentName.setCallback(self.onTextEnter)
		
		##Edit due date
		self.dateLabel = "Due date:"
		self.datePos = (2, 2)
		self.editDate = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 20,
			sizeYX = (1, 23),
			positionYX = (self.datePos[0], self.datePos[1] + len(self.dateLabel) + 1))
		self.editDate.setCallback(self.onTextEnter)
		
		##Edit number of late
		self.lateLabel = "Number of allowed late days:"
		self.latePos = (3, 2)
		self.editLate = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 3,
			sizeYX = (1, 6),
			positionYX = (self.latePos[0], self.latePos[1] + len(self.lateLabel) + 1))
		self.editLate.setCallback(self.onTextEnter)
		
		##Edit max number of submissions
		self.maxSubmissionsLabel = "Number of allowed submissions"
		self.maxSubmissionsPos = (4, 2)
		self.editMaxSubmissions = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 3,
			sizeYX = (1, 6),
			positionYX = (self.maxSubmissionsPos[0], self.maxSubmissionsPos[1] + len(self.maxSubmissionsLabel) + 1))
		self.editMaxSubmissions.setCallback(self.onTextEnter)
		
		##Save button.
		self.savePos = (5, 2)
		self.saveBtn = Button.Button(
			parent = self.editPanel,
			positionYX = self.savePos,
			label = "Save Changes")
		self.saveBtn.setCallback(self.onBtnSaveGrade)
		pass
			
	
	def _createGradeEditPanel(self, size, pos):
		self.editGradeVisible = False
		# Edit grade
		self.gradeLabel = "Score:"
		self.gradePos = (1, 2)
		self.editGrade = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 6,
			sizeYX = (1, 9),
			positionYX = (self.gradePos[0], self.gradePos[1] + len(self.gradeLabel) + 1))
		self.editGrade.setCallback(self.onTextEnter)
		
		# Edit comment
		self.commentLabel = "Comments:"
		self.commentPos = (2, 2)
		self.editComment = TextEditField.TextEditField(
			self.editPanel,
			maxLength = 42,
			sizeYX = (1, 45),
			positionYX = (self.commentPos[0] + 1, self.commentPos[1] + 1))
		self.editComment.setCallback(self.onTextEnter)
		
		# Save button.
		self.savePos = (5, 2)
		self.saveBtn = Button.Button(
			parent = self.editPanel,
			positionYX = self.savePos,
			label = "Save Changes")
		self.saveBtn.setCallback(self.onBtnSaveAssignment)
	
	def _clearAssignmentPanel(self):
		self.editPanel.clear()
		self.editPanel.refresh()
	
	def _drawAssignmentEditPanel(self):
		self.editPanel.clear()
		
		##Edit assignment name
		self.editPanel.addstr(self.assignmentNamePos[0], self.assignmentNamePos[1], self.assignmentNameLabel)
		self.editAssignmentName.redraw()
		
		##Edit due date
		self.editPanel.addstr(self.datePos[0], self.datePos[1], self.dateLabel)
		self.editDate.redraw()

		##Edit number of late days
		self.editPanel.addstr(self.latePos[0], self.latePos[1], self.lateLabel)
		self.editLate.redraw()
		
		##Edit number of allowed submissions
		self.editPanel.addstr(self.maxSubmissionsPos[0], self.maxSubmissionsPos[1], self.maxSubmissionsLabel)
		self.editMaxSubmissions.redraw()
		
		##Save button
		self.saveBtn.redraw()
		
		##Set up input manager
		if not self.editAssignmentVisible:
			self.inputManager.addElement(self.editAssignmentName)
			self.inputManager.addElement(self.editDate)
			self.inputManager.addElement(self.editLate)
			self.inputManager.addElement(self.editMaxSubmissions)
			self.inputManager.addElement(self.saveBtn)
			self.editAssignmentVisible = True
		
		self.editPanel.box()
		self.editPanel.refresh()
		pass
	
	def _drawGradeEditPanel(self):
		self.editPanel.clear()
		
		# Edit grade
		self.editPanel.addstr(self.gradePos[0], self.gradePos[1], self.gradeLabel)
		self.editGrade.redraw()
		
		# Edit comment
		self.editPanel.addstr(self.commentPos[0], self.commentPos[1], self.commentLabel)
		self.editComment.redraw()

		# Save button
		self.saveBtn.redraw()
		
		# Set up input manager
		if not self.editGradeVisible:
			self.inputManager.addElement(self.editGrade)
			self.inputManager.addElement(self.editComment)
			self.inputManager.addElement(self.saveBtn)
			self.editGradeVisible = True
		
		self.editPanel.box()
		self.editPanel.refresh()
		pass

	def _drawStudent(self):
		
		try:
			#pass
			#options = self.parent.submissionManager.getCourseList(),
			#TODO: actually need to get the grade here
			#studentScore = self.parent.GradeConfigManager.getGrade(self, "test")
			# test_file = "../test/testCourse/testProject/student1/Grade.config"
			# f = open(test_file)
			# lines=f.readlines()
			# studentScore = lines[1][8:]
			# bonus = lines[2][8:]
			# total = int(studentScore) + int(bonus)
			# feedback = lines[3][11:]
			# #mean = 100
			# #median = 100
			# #sd = 0
			
			# self.pickFiles = Picker.Picker(
			# 	parent = self.panelMain,
			# 	positionYX = (1, int((self.screenSize[1] - 4) / 3) + 1),
			# 	sizeYX = (self.screenSize[0] - 9,
			# 		2 * int((self.screenSize[1] - 3) / 3)),
			# 	title = 'Grade and Statistics',
			# 	#arrow="",
			# 	options = ["Your score: "+str(studentScore), "Bonus: "+str(bonus), "Total: "+str(total), "Feedback: "+feedback#, "", "Statistics", "", "Mean: "+str(mean), "Median: "+str(median), "Standard Deviation: "+str(sd)
			# 	],
			# 	footer = "",
			# 	maxSelect = 1,
			# 	c_empty = "",
			# 	c_selected = "")
			#self.pickFiles.redraw()
			#self.inputManager.addElement(self.pickFiles)

			# Add Grades button.
			self.btnExit = Button.Button(
				parent = self.panelMain,
				positionYX = (self.screenSize[0] - 8,
					2 * int((self.screenSize[1] - 4) / 3) - 4),
				label = "Exit")
			self.btnExit.setCallback(exit, 0)
			self.btnExit.redraw()
			
			# # File picker.
			# self.pickFiles = Picker.Picker(
				# parent = self.panelMain,
				# positionYX = (1, int((self.screenSize[1] - 4) / 3) + 1),
				# sizeYX = (self.screenSize[0] - 9,
					# 2 * int((self.screenSize[1] - 3) / 3)),
				# title = 'Files',
				# options = [self._getFileList(SUBMISSION_FOLDER)],
				# footer = "",
				# maxSelect = -1,
				# c_empty = "[ ]",
				# c_selected = "[X]")
			# self.pickFiles.redraw()
			# self.inputManager.addElement(self.pickFiles)
		except Exception as err:
			raise err
	
	def _drawUpdate(self):
		try:
			# Get user input and handle interaction.
			inputChar = self.screenMain.getch()
			if inputChar != -1:
				# Update list widgets.
				inp = self.inputManager.onInput(inputChar)
				self.inputManager.currentElement.redraw()
		
			# Update time panel.
			self.panelTime.addstr(1, 0, time.strftime("%I:%M:%S %p"))
			self.panelTime.refresh()
		except Exception as err:
			raise err
	
	def displayMessage(self, message, textAttr=curses.A_NORMAL):
		blank = ""
		for i in range(0, self.lastMsgLen):
			blank += " "
		self.panelMain.addstr(
			self.screenSize[0] - 5, 2,
			blank,
			curses.A_NORMAL)
		self.lastMsgLen = len(message)
		self.panelMain.addstr(
			self.screenSize[0] - 5, 2,
			message,
			textAttr)
		self.panelMain.refresh()
	
	def onSelectCourse(self):
		selected = self.pickCourse.getSelected()
		if len(selected) == 1:
			course = selected[0]
			if self.course != course:
				self.course = course
				assignments = self.parent.courseManager.getAssignmentList(course)
				
				# Add the "New Assignment" Feature.
				if self.mode is MODE_INSTRUCTOR:
					assignments.insert(0, "<---NEW ASSIGNMENT--->")
					assignments.insert(0, "<---OVERALL GRADES--->")
				
				self.pickAssignment.setOptions(assignments)
				self.pickAssignment.redraw()
				
				if self.mode is MODE_INSTRUCTOR:				
					self.pickStudent.setOptions(self._getStudentList(course))
					self.pickStudent.redraw()
				
				if not self.pickAssignmentVisible:
					self.pickAssignmentVisible = True
					self.inputManager.addElement(self.pickAssignment)
	
	def onSelectAssignment(self):
		selected = self.pickAssignment.getSelected()
		##self.displayMessage("Made it into the right function")
		if len(selected) == 1:
			assignment = selected[0]
			if self.assignment != assignment:
			##	self.displayMessage("Got an assignment")
				self.assignment = assignment
				self.displayMessage("The assignment is " + assignment)
				if self.mode is MODE_INSTRUCTOR and assignment == "<---NEW ASSIGNMENT--->":
					##self.displayMessage("Made it into the right if statement")
					self._drawAssignmentEditPanel()
					
				if self.mode is MODE_INSTRUCTOR and not self.pickStudentVisible:
					self.pickStudentVisible = True
					self.pickStudent.redraw()
					self.inputManager.addElement(self.pickStudent)
				if self.mode is MODE_STUDENT:
					studentScore = self.parent.courseManager.getGrade(self.course, self.assignment, self.student)
					bonus = self.parent.courseManager.getBonus(self.course, self.assignment, self.student)
					total = float(studentScore) + float(bonus)
					feedback = self.parent.courseManager.getFeedback(self.course, self.assignment, self.student)
					if studentScore is False:
						studentScore = "None yet."
						total = "None yet."
					if bonus is False:
						bonus = "None yet."
					if feedback is False:
						feedback = "None yet."

					self.pickFiles = Picker.Picker(
					parent = self.panelMain,
					positionYX = (1, int((self.screenSize[1] - 4) / 3) + 1),
					sizeYX = (self.screenSize[0] - 9,
						2 * int((self.screenSize[1] - 3) / 3)),
					title = 'Grade and Statistics',
					#arrow="",
					options = ["Your score: "+str(studentScore), "Bonus: "+str(bonus), "Total: "+str(total), "Feedback: "+str(feedback)#, "", "Statistics", "", "Mean: "+str(mean), "Median: "+str(median), "Standard Deviation: "+str(sd)
					],
					footer = "",
					maxSelect = 1,
					c_empty = "",
					c_selected = "")
					self.pickFiles.redraw()
					self.inputManager.addElement(self.pickFiles)
					self.inputManager.addElement(self.btnExit)
	
	def onSelectStudent(self):
		selected = self.pickStudent.getSelected()
		if len(selected) == 1:
			student = selected[0]
			if self.student != student:
				self.student = student
				self.displayAssignmentInfo(self.course, self.assignment, self.student)
	
	def _getStudentList(self, course):
		try:
			groupName = self.parent.courseManager.getCourseUserGroup(course)
			group = grp.getgrnam(groupName).gr_mem
		except KeyError:
			raise ProgramException.ConfigurationInvalid("Group does not exist for " + course)
		result = []
		for user in group:
			grade = self.parent.courseManager.getGrade(self.course, self.assignment, self.student)
			line = user
			blank = ""
			for i in range(self.studentPanelSizeYX[1] - 10):
				blank += " "
			if grade != False:
				line += blank + str(grade)
			result.append(line)
		return result
	
	def displayAssignmentInfo(self, course, assignment, student):
		self.displayMessage("Learning about " + student)
		self._drawGradeEditPanel()
	
	def onTextEnter(self):
		return "TAB_NEXT"
	
	def onBtnSaveGrade(self):
		try:
			grade = float(self.editGrade.getValue())
		except ValueError:
			self.displayMessage("Please enter a score as a real number.")
			return
		result = self.parent.courseManager.editGrade(
			self.course,
			self.assignment,
			self.student,
			grade)
		if result:
			self.parent.courseManager.editFeedback(
				self.course,
				self.assignment,
				self.student,
				self.editComment.getValue())
			self._clearAssignmentPanel()
			self.displayMessage("Grade updated!")
		else:
			self.displayMessage("ERROR: Grade not saved.")
		
	def onBtnSaveAssignment(self): #{
		## editAssignmentName editDate editLate
		try:
			assignmentName = self.editAssignmentName.getValue()
			dueDate = self.editDate.getValue()
			lateDays = self.editLate.getValue()
			maxSubmissions = self.editMaxSubmissions.getValue()
		except ValueError:
			self.displayMessage("Error parsing assignment input")
			return
		
		check = self.parent.courseManager.createAssignment(self.course, assignmentName, dueDate, False, maxSubmissions, lateDays)
		
		if check:
			self.displayMessage("Assignment created")
			self._clearAssignmentPanel()
			assignments = self.parent.courseManager.getAssignmentList(self.course)				
			# Add the "New Assignment" Feature.
			if self.mode is MODE_INSTRUCTOR:
				assignments.insert(0, "<---NEW ASSIGNMENT--->")
			self.pickAssignment.setOptions(assignments)
			self.pickAssignment.redraw()
		else:
			self.displayMessage("Assignment not created")
		pass
	#}
