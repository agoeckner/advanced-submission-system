#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import time
import InputManager
import Picker

PROGRAM_TITLE = "ADVANCED SUBMISSION SYSTEM"
PROGRAM_SUBTITLE = "Purdue Computer Science"
INTERFACE_TITLE = "SUBMIT ASSIGNMENT"

# SubmissionInterface is used to submit assignments.
class SubmissionInterface:

	parent = None
	inputManager = None

	# UI elements.
	screenMain = None
	screenSize = (0, 0)
	panelTop = None
	panelInfo = None
	panelTime = None
	pickCourse = None
	pickAssignment = None

	def __init__(self, parent):
		self.parent = parent
		self.inputManager = InputManager.InputManager(self)
	
	def show(self):
		try:
			curses.wrapper(self._draw)
		except KeyboardInterrupt:
			raise
		except Exception as err:
			print("curseserror: " + str(err))
			raise
	
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
				c_selected = "(X)",
				arrow = "==>")
			self.pickCourse.redraw()
			self.inputManager.addElement(self.pickCourse)
			
			# Assignment picker.
			self.pickAssignment = Picker.Picker(
				parent = self.panelMain,
				positionYX = (pickCourseSizeY + 1, 1),
				sizeYX = (self.screenSize[0] - 5 - pickCourseSizeY,
					int((self.screenSize[1] - 4) / 3)),
				title = 'Assignment',
				options = ["lab1", "lab2"],
				footer = "",
				maxSelect = 1,
				c_empty = "( )",
				c_selected = "(X)",
				arrow = "==>")
			self.pickAssignment.redraw()
			self.inputManager.addElement(self.pickAssignment)

			# UI Loop
			while True:
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