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
	startingList = ["a", "b", "c"]

	def setUp(self):
		self.stdscr = curses.initscr()
		curses.endwin()
		self.picker = Picker.Picker(self.stdscr, 
			(0, 0), 
			(10, 10), 
			self.startingList)

	def test_set_options_list(self):
		opts = ["1", "2", "3"]
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
	
	def test_select_no_callback(self):
		self.callbackUpdate = ""
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(selected, ["a"])
		self.assertEqual(self.callbackUpdate, "")
	
	def test_select_callback(self):
		self.callbackUpdate = ""
		self.picker.setCallback(self.pickerCallback, "test")
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(selected, ["a"])
		self.assertEqual(self.callbackUpdate, "testing")

	def test_select_none(self):
		selected = self.picker.getSelected()
		self.assertEqual(selected, [])

	def test_select_multiple(self):
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(selected, self.startingList[0:3])

	def test_select_tree_parent(self):
		opts = ["a", ("b",[("1", ["test"]), "2", "3"]), "c"]
		self.picker.setOptions(opts)
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		expected = ["b", "1", "test", "2", "3"]
		selected = self.picker.getSelected()
		self.assertEqual(expected, selected)
	
	def test_deselect_tree_parent(self):
		opts = ["a", ("b",[("1", ["test"]), "2", "3"]), "c"]
		self.picker.setOptions(opts)
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		expected = ["b", "1", "test", "2", "3"]
		selected = self.picker.getSelected()
		self.assertEqual(expected, selected)
		self.picker.onInput(ord(' '))
		expected = []
		selected = self.picker.getSelected()
		self.assertEqual(expected, selected)
	
	def test_select_max_1(self):
		self.picker.maxSelect = 1
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual([self.startingList[2]], selected)

	def test_select_max_gt_1(self):
		self.picker.maxSelect = 2
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(self.startingList[0:2], selected)
	
	def test_deselect_max_gt_1(self):
		self.picker.maxSelect = 2
		self.picker.onInput(ord(' '))
		self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(self.startingList[0:2], selected)
		self.picker.onInput(ord(' '))
		selected = self.picker.getSelected()
		self.assertEqual(self.startingList[0:1], selected)

	def test_cursor_min(self):
		self.picker.onInput(curses.KEY_UP)
		self.assertEqual(1, self.picker.cursor)
		self.picker.onInput(curses.KEY_UP)
		self.assertEqual(1, self.picker.cursor)
	
	def test_cursor_max(self):
		for opt in self.startingList:
			self.picker.onInput(curses.KEY_DOWN)
		self.picker.onInput(curses.KEY_DOWN)
		self.assertEqual(len(self.startingList), self.picker.cursor)
		self.picker.onInput(curses.KEY_UP)
		self.assertEqual(len(self.startingList) - 1, self.picker.cursor)

	def pickerCallback(self, a):
		self.callbackUpdate = a + "ing"
		
if __name__ == '__main__':
	unittest.main()