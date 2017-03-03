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
import ui.TextEditField as TextEditField

class TestUITextEditField(unittest.TestCase):
	def setUp(self):
		self.stdscr = curses.initscr()
		curses.endwin()
		self.text = TextEditField.TextEditField(
			self.stdscr,
			maxLength = 8,
			sizeYX = (1, 15))
		
	def test_default_value(self):
		text = TextEditField.TextEditField(
			self.stdscr,
			defaultValue = "test",
			sizeYX = (1, 10))
		result = text.getValue()
		self.assertEqual(result, "test")
	
	def test_size_invalid(self):
		with self.assertRaises(ProgramException.ComponentSizeInvalid):
			text = TextEditField.TextEditField(
				self.stdscr,
				sizeYX = (1, 3))
	
	def test_max_length_invalid(self):
		with self.assertRaises(ProgramException.ComponentSizeInvalid):
			text = TextEditField.TextEditField(
				self.stdscr,
				maxLength = 8,
				sizeYX = (1, 10))
	
	def test_input_min_size(self):
		text = TextEditField.TextEditField(
			self.stdscr,
			sizeYX = (1, 4))
		self.text.onInput(ord('a'))
		result = text.getValue()
		self.assertEqual(result, "a")
	
	def test_input_none(self):
		result = self.text.getValue()
		self.assertEqual(result, "")
	
	def test_input_word(self):
		self.text.onInput(ord('b'))
		self.text.onInput(ord('l'))
		self.text.onInput(ord('a'))
		self.text.onInput(ord('h'))
		result = self.text.getValue()
		self.assertEqual(result, "blah")
	
	def test_input_word(self):
		self.text.onInput(ord('a'))
		self.text.onInput(ord(' '))
		self.text.onInput(ord('t'))
		self.text.onInput(ord('e'))
		self.text.onInput(ord('s'))
		self.text.onInput(ord('t'))
		result = self.text.getValue()
		self.assertEqual(result, "a test")
	
	def test_input_gt_max(self):
		expected = ""
		for i in range(0, self.text.maxLength + 1):
			expected += 'a'
			self.text.onInput(ord('a'))
		expected = expected[0:self.text.maxLength]
		result = self.text.getValue()
		self.assertEqual(result, expected)
	
	def test_input_eq_max(self):
		expected = ""
		for i in range(0, self.text.maxLength):
			expected += 'a'
			self.text.onInput(ord('a'))
		expected = expected[0:self.text.maxLength]
		result = self.text.getValue()
		self.assertEqual(result, expected)

	def test_enter_no_callback(self):
		with self.assertRaises(ProgramException.MissingCallback):
			result = self.text.onInput(ord('\n'))
	
	def test_enter_callback(self):
		self.text.setCallback(callback)
		result = self.text.onInput(ord('\n'))
		self.assertEqual(result, 52)

	def test_enter_callback_args(self):
		a = 59
		b = 11
		c = 99
		self.text.setCallback(callbackArgs, a, b, named=c)
		result = self.text.onInput(ord('\n'))
		self.assertEqual(result, a + b + c)

def callback():
	return 52

def callbackArgs(a, b, named = 11):
	return a + b + named

if __name__ == '__main__':
	unittest.main()