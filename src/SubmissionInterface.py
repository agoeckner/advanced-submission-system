#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import time

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
		print("Showing Submission UI")
		try:
			curses.wrapper(self._draw)
		except Exception as err:
			print("curseserror: " + str(err))
	
	def _draw(self, stdscr):
		self.screenMain = stdscr
		try:
			# UI Setup
			self.screenSize = stdscr.getmaxyx()
			curses.curs_set(0)
			# stdscr.hline(2, 0, curses.ACS_HLINE, self.screenSize[1])
			stdscr.refresh()
			
			# Top panel.
			self.panelTop = curses.newwin(2, self.screenSize[1], 0, 0)
			
			# Information panel on the left of the top panel.
			self.panelInfo = self.panelTop.derwin(2, self.screenSize[1] - 12, 0, 0)
			self.panelInfo.addstr(0, 0, "ADVANCED SUBMISSION SYSTEM", curses.A_STANDOUT)
			self.panelInfo.addstr(1, 3, "Purdue Computer Science", curses.A_DIM)
			self.panelInfo.addstr(1, 35, "SUBMIT ASSIGNMENT", curses.A_NORMAL)
			self.panelInfo.refresh()
			
			# Time panel in the top-right corner.
			self.panelTime = self.panelTop.derwin(2, 12, 0, self.screenSize[1] - 12)
			self.panelTime.addstr(0, 0, "Current Time", curses.A_UNDERLINE)
			
			# Main panel.
			self.panelMain = curses.newwin(self.screenSize[0] - 2, self.screenSize[1], 2, 0)
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