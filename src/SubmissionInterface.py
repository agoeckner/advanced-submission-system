#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import time

PROGRAM_TITLE = "ADVANCED SUBMISSION SYSTEM"
PROGRAM_SUBTITLE = "Purdue Computer Science"
INTERFACE_TITLE = "SUBMIT ASSIGNMENT"

# SubmissionInterface is used to submit assignments.
class SubmissionInterface:

	# UI elements.
	screenMain = None
	screenSize = (0, 0)
	panelTop = None
	panelInfo = None
	panelTime = None

	def __init__(self):
		pass
	
	def show(self):
		try:
			curses.wrapper(self._draw)
		except KeyboardInterrupt:
			raise
		except Exception as err:
			print("curseserror: " + str(err))
	
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

			# UI Loop
			while True:
				self._drawUpdate()
				# No need to refresh faster than 1 FPS for this example...
				time.sleep(1)
		except Exception as err:
			raise err

	def _drawUpdate(self):
		try:
			# Update time panel.
			self.panelTime.addstr(1, 0, time.strftime("%I:%M:%S %p"))
			self.panelTime.refresh()
		except Exception as err:
			raise err