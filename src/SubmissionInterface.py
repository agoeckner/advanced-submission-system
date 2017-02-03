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
		
		# Information panel in the top-left corner.
		infoPanel = curses.newwin(2, int(termSize[1] / 2), 0, 0)
		infoPanel.addstr(0, 0, "ADVANCED SUBMISSION SYSTEM", curses.A_STANDOUT)
		infoPanel.addstr(1, 0, "   Purdue Computer Science", curses.A_DIM)
		infoPanel.refresh()
		
		# Time panel in the top-right corner.
		timePanel = curses.newwin(2, 12, 0, termSize[1] - 12)
		timePanel.addstr(0, 0, "Current Time", curses.A_UNDERLINE)

		# UI Loop
		while True:
			# Update time panel.
			timePanel.addstr(1, 0, time.strftime("%I:%M:%S %p"))
			timePanel.refresh()

			# stdscr.refresh()
			# stdscr.getkey()
			
			# No need to refresh faster than 1 FPS for this example...
			time.sleep(1)