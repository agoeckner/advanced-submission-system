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
		while True:
			# Clear screen
			stdscr.clear()

			stdscr.addstr("Current time:\n")
			stdscr.addstr("    " + time.strftime("%H:%M:%S"))

			stdscr.refresh()
			# stdscr.getkey()