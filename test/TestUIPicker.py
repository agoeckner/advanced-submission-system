#=================================
# Advanced Submission System
# CS 40800 - Software Engineering
# Purdue University
#=================================

import sys
sys.path.append('../src/')
import unittest
import curses
import ui.Picker as Picker

class TestUIPicker(unittest.TestCase):
	def setUp(self):
		self.stdscr = curses.initscr()
		curses.endwin()
		self.picker = Picker.Picker(self.stdscr, 
			(0, 0), 
			(10, 10), 
			["a", "b"])

	def test_set_options_list(self):
		opts = ["a", "b", "c"]
		self.picker.setOptions(opts)
		pickerOpts = list(map(lambda x: x["label"], self.picker.all_options))
		self.assertEqual(opts, pickerOpts)
	
	def test_set_options_tree(self):
		opts = ["a", ("b",[("1", ["test"]), "2", "3"]), "c"]
		self.picker.setOptions(opts)
		
		expected = [
			{"label": "a", "level": 0, "selected": False, "isParent": False},
			{"label": "b", "level": 0, "selected": False, "isParent": True},
			{"label": "1", "level": 1, "selected": False, "isParent": True},
			{"label": "test", "level": 2, "selected": False, "isParent": False},
			{"label": "2", "level": 1, "selected": False, "isParent": False},
			{"label": "3", "level": 1, "selected": False, "isParent": False},
			{"label": "c", "level": 0, "selected": False, "isParent": False}]
		result = self.picker.all_options
		self.assertEqual(expected, result)

if __name__ == '__main__':
	unittest.main()