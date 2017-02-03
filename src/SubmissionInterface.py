#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import curses
import time

# SubmissionInterface is used to submit assignments.
class SubmissionInterface:
	def __init__(self):
		pass
	
	def show(self):
		print("Showing Submission UI")
		
		curses.wrapper(self.uiLoop)
	
	def uiLoop(self, stdscr):
		# UI Setup
		curses.curs_set(0)
		testWindow = curses.newwin(5, 40, 5, 5)
		
		# UI Loop
		while True:
			# Clear screen
			testWindow.clear()
			testWindow.border(1)
			testWindow.box()

			testWindow.addstr("Current time:\n", curses.A_REVERSE)
			testWindow.addstr("    " + time.strftime("%H:%M:%S"))

			stdscr.refresh()
			testWindow.refresh()
			# stdscr.getkey()
			
			# No need to refresh faster than 1 FPS for this example...
			time.sleep(1)