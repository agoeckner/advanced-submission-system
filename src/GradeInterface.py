#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import time
import ui.Button as Button
import ui.InputManager as InputManager
import ui.Picker as Picker

PROGRAM_TITLE = "ADVANCED SUBMISSION SYSTEM"
PROGRAM_SUBTITLE = "Purdue Computer Science"
INTERFACE_TITLE = "GRADES"

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
			self.panelInfo.addstr(1, 3, PROGRAM_SUBTITLE, curses.A_DIM)
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
				options = self.parent.submissionManager.getCourseList(),
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
			self.inputManager.addElement(self.pickAssignment)
			
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
			# Student list panel.
			studentPanelSizeYX = (self.screenSize[0] - 20, 2 * int((self.screenSize[1] - 3) / 3))
			self.studentPanel = self.panelMain.derwin(
				studentPanelSizeYX[0], studentPanelSizeYX[1], # size
				1, int((self.screenSize[1] - 4) / 3) + 1) # position
			self.studentPanel.bkgd(curses.color_pair(1))
			centerTip = "Please select a course to view grades."
			self.studentPanel.addstr(
				int(studentPanelSizeYX[0] / 2),
				int(studentPanelSizeYX[1] / 2) - int(len(centerTip) / 2),
				centerTip,
				curses.A_DIM)
			self.studentPanel.box()
			self.studentPanel.refresh()
			
			# Assignment edit panel.
			editPanelSizeYX = (self.screenSize[0] - 23, 2 * int((self.screenSize[1] - 3) / 3))
			self.editPanel = self.panelMain.derwin(
				editPanelSizeYX[0], editPanelSizeYX[1], # size
				studentPanelSizeYX[0] + 1, int((self.screenSize[1] - 4) / 3) + 1) # position
			self.editPanel.bkgd(curses.color_pair(1))
			centerTip = "Assignment options are changed here."
			self.editPanel.addstr(
				int(editPanelSizeYX[0] / 2),
				int(editPanelSizeYX[1] / 2) - int(len(centerTip) / 2),
				centerTip,
				curses.A_DIM)
			self.editPanel.box()
			self.editPanel.refresh()
			
		except Exception as err:
			raise err

	def _drawStudent(self):
		try:
			pass
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
		self.panelMain.addstr(
			self.screenSize[0] - 5,
			int((self.screenSize[1] - 4) / 3) + 2,
			message,
			textAttr)
		self.panelMain.refresh()
	
	def onSelectCourse(self):
		selected = self.pickCourse.getSelected()
		if len(selected) == 1:
			course = selected[0]
			if self.course != course:
				self.course = course
				assignments = self.parent.submissionManager.getAssignmentList(course)
				
				# Add the "New Assignment" Feature.
				if self.mode is MODE_INSTRUCTOR:
					assignments.insert(0, "<---NEW ASSIGNMENT--->")
					assignments.insert(0, "<---OVERALL GRADES--->")
				
				self.pickAssignment.setOptions(assignments)
				self.pickAssignment.redraw()
	
	def onSelectAssignment(self):
		selected = self.pickAssignment.getSelected()
		if len(selected) == 1:
			assignment = selected[0]
			if self.assignment != assignment:
				self.assignment = assignment
