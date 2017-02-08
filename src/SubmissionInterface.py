#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import os
import os.path
import time
import ui.Button as Button
import ui.InputManager as InputManager
import ui.Picker as Picker

PROGRAM_TITLE = "ADVANCED SUBMISSION SYSTEM"
PROGRAM_SUBTITLE = "Purdue Computer Science"
INTERFACE_TITLE = "SUBMIT ASSIGNMENT"
SUBMISSION_FOLDER = os.getcwd()

# SubmissionInterface is used to submit assignments.
class SubmissionInterface:

	parent = None
	inputManager = None
	run = True

	# UI elements.
	screenMain = None
	screenSize = (0, 0)
	panelTop = None
	panelInfo = None
	panelTime = None
	pickCourse = None
	pickAssignment = None
	pickFile = None
	btnSubmit = None

	def __init__(self, parent):
		self.parent = parent
		self.inputManager = InputManager.InputManager(self)
	
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
			# stdscr.hline(2, 0, curses.ACS_HLINE, self.screenSize[1])
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
				self.screenSize[0] - 6,
				self.screenSize[1] - 36,
				"Tip: Use the spacebar to select.",
				curses.A_DIM)
			self.panelMain.box()
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
			self.inputManager.addElement(self.pickCourse)
			
			# Assignment picker.
			self.pickAssignment = Picker.Picker(
				parent = self.panelMain,
				positionYX = (pickCourseSizeY + 1, 1),
				sizeYX = (self.screenSize[0] - 6 - pickCourseSizeY,
					int((self.screenSize[1] - 4) / 3)),
				title = 'Assignment',
				options = ["lab1", "lab2"],
				footer = "",
				maxSelect = 1,
				c_empty = "( )",
				c_selected = "(X)")
			self.pickAssignment.redraw()
			self.inputManager.addElement(self.pickAssignment)
			
			# File picker.
			self.pickFiles = Picker.Picker(
				parent = self.panelMain,
				positionYX = (1, int((self.screenSize[1] - 4) / 3) + 1),
				sizeYX = (self.screenSize[0] - 9,
					2 * int((self.screenSize[1] - 3) / 3)),
				title = 'Files',
				options = [self._getFileList(SUBMISSION_FOLDER)],
				footer = "",
				maxSelect = -1,
				c_empty = "[ ]",
				c_selected = "[X]")
			self.pickFiles.redraw()
			self.inputManager.addElement(self.pickFiles)
			
			# Submit button.
			self.btnSubmit = Button.Button(
				parent = self.panelMain,
				positionYX = (self.screenSize[0] - 8,
					2 * int((self.screenSize[1] - 4) / 3) - 4),
				label = "SUBMIT")
			self.btnSubmit.setCallback(self.onBtnSubmit)
			self.btnSubmit.redraw()
			self.inputManager.addElement(self.btnSubmit)

			# UI Loop
			while self.run:
				self._drawUpdate()
				# No need to refresh faster than 1 FPS for this example...
				time.sleep(0.01)
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
			self.screenSize[0] - 7,
			int((self.screenSize[1] - 4) / 3) + 2,
			message,
			textAttr)
		self.panelMain.refresh()
	
	def onBtnSubmit(self):
		# self.run = False
		course = self.pickCourse.getSelected()
		assignment = self.pickAssignment.getSelected()
		files = self.pickFiles.getSelected()
		if len(course) != 1:
			self.displayMessage("Please select a course.", curses.A_STANDOUT)
			return
		elif len(assignment) != 1:
			self.displayMessage("Please select an assignment.", curses.A_STANDOUT)
			return
		elif len(files) < 1:
			self.displayMessage("Please select at least one file.", curses.A_STANDOUT)
			return
		self.displayMessage("                                ") # clear message
		
		# Submit the assignment.
		course = course[0]
		assignment = assignment[0]
		if self.parent.submissionManager.submitAssignment(course, assignment, files):
			# Execution done.
			self.run = false
		else:
			self.displayMessage("ERROR: Submission failed.", curses.A_STANDOUT)
	
	def _getFileList(self, directory):
		dirName = directory
		dirList = []
		
		for entry in sorted(os.listdir(directory), key = str.lower):
			if os.path.isdir(entry):
				dirList.append(self._getFileList(entry))
			else:
				dirList.append(entry)
		
		return (dirName, dirList)