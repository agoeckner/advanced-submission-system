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
		
		curses.wrapper(self.draw)
	
	def draw(self, stdscr):
		# UI Setup
		termSize = stdscr.getmaxyx()
		curses.curs_set(0)
		stdscr.hline(2, 0, curses.ACS_HLINE, termSize[1])
		stdscr.refresh()
		
		# Top information panels.
		topWindow = curses.newwin(2, termSize[1], 0, 0)
		topWindow.addstr(0, termSize[1] - 12, "Current Time", curses.A_UNDERLINE)

		# UI Loop
		while True:
			# Update top window.
			# topWindow.clear()
			topWindow.addstr(1, termSize[1] - 12, time.strftime("%I:%M:%S"))
			topWindow.refresh()

			# stdscr.refresh()
			# stdscr.getkey()
			
			# No need to refresh faster than 1 FPS for this example...
			time.sleep(1)