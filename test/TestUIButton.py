#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import curses
import ProgramException
import ui.Button as Button

class TestUIButton(unittest.TestCase):
	def setUp(self):
		self.stdscr = curses.initscr()
		curses.endwin()
		self.button = Button.Button(
			self.stdscr,
			"test")
		
	def test_input_nonselect(self):
		result = self.button.onInput(ord('a'))
		self.assertEqual(result, None)
	
	def test_select_no_callback(self):
		with self.assertRaises(ProgramException.MissingCallback):
			result = self.button.onInput(ord(' '))
	
	def test_select_callback(self):
		self.button.setCallback(buttonCallback)
		result = self.button.onInput(ord(' '))
		self.assertEqual(result, 52)
	
	# Tests a Select input when no callback is refined.
	def test_select_callback_args(self):
		a = 59
		b = 11
		c = 99
		self.button.setCallback(buttonCallbackArgs, a, b, named=c)
		result = self.button.onInput(ord(' '))
		self.assertEqual(result, a + b + c)

def buttonCallback():
	return 52

def buttonCallbackArgs(a, b, named = 11):
	return a + b + named

if __name__ == '__main__':
	unittest.main()