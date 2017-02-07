# This code is available for use under CC0 (Creative Commons 0 - universal). 
# You can copy, modify, distribute and perform the work, even for commercial
# purposes, all without asking permission. For more information, see LICENSE.md or 
# https://creativecommons.org/publicdomain/zero/1.0/

# Original Source: https://github.com/pp19dd/picker

# usage:
# opts = Picker(
#    title = 'Delete all files',
#    options = ["Yes", "No"]
# ).getSelected()

# returns a simple list
# cancel returns False

import curses

class Picker:
	"""Allows you to select from a list with curses"""
	stdscr = None
	win = None
	title = ""
	arrow = ""
	footer = ""
	more = ""
	c_selected = ""
	c_empty = ""
	maxSelect = -1
	tempArrow = ""
	
	cursor = 0
	offset = 0
	selected = 0
	selcount = 0
	aborted = False
	
	window_height = 0
	window_width = 0
	all_options = []
	length = 0

	def getSelected(self):
		if self.aborted == True:
			return( False )

		ret_s = filter(lambda x: x["selected"], self.all_options)
		ret = list(map(lambda x: x["label"], ret_s))
		return( ret )
		
	def redraw(self):
		self.win.clear()
		
		# Don't add dots on selected items
		# if self.offset > 0:
			# if self.all_options[self.offset]["selected"]:
				# self.offset -= 1
			# elif self.all_options[self.offset+self.window_height-2]["selected"]:
				# self.offset += 1
		
		position = 1
		range = self.all_options[self.offset:self.offset+self.window_height-1]
		for option in range:
			if option["selected"] == True:
				line_label = self.c_selected + " "
			else:
				line_label = self.c_empty + " "
			
			self.win.addstr(position, 5, line_label + option["label"])
			position = position + 1
			
		# hint for more content above
		if self.offset > 0:
			self.win.addstr(1, 5, self.more)
		
		# hint for more content below
		#TODO
		if self.offset + self.window_height <= self.length:
			self.win.addstr(self.window_height - 2, 5, self.more)
		
		self.win.box()
		if(len(self.footer) > 0):
			self.win.addstr(
				self.window_height - 1, 2, " " + self.footer + " "
			)
		if len(self.title) > 0:
			self.win.addstr(0, 1, " " + self.title + " ")
		if self.maxSelect != 1:
			self.win.addstr(
				0, self.window_width - 8,
				" " + str(self.selcount) + "/" + str(self.length) + " "
			)
		self.win.addstr(self.cursor,1, self.arrow)
		self.win.refresh()
	
	def cursorDown(self):
		if self.cursor >= self.length:
			return

	def check_cursor_up(self):
		if self.cursor < 1:
			self.cursor = 1
			if self.offset > 0:
				self.offset = self.offset - 1
	
	def check_cursor_down(self):
		if self.cursor > self.length:
			self.cursor = self.cursor - 1
	
		if self.cursor >= self.window_height - 1:
			self.cursor = self.window_height - 2
			self.offset = self.offset + 1
			
			if self.offset + self.cursor > self.length:
				self.offset = self.offset - 1
	
	def onInput(self, c):
		if c == curses.KEY_UP:
			self.cursor = self.cursor - 1
		elif c == curses.KEY_DOWN:
			self.cursor = self.cursor + 1
		#elif c == curses.KEY_PPAGE:
		#elif c == curses.KEY_NPAGE:
		elif c == ord(' '):
			if self.maxSelect == 1:
				for opt in filter(lambda x: x["selected"], self.all_options):
					opt["selected"] = False
			self.all_options[self.selected]["selected"] = \
				not self.all_options[self.selected]["selected"]
		elif c == 10:
			return
				
		# deal with interaction limits
		self.check_cursor_up()
		self.check_cursor_down()

		# compute selected position only after dealing with limits
		self.selected = self.cursor + self.offset - 1
		
		temp = self.getSelected()
		self.selcount = len(temp)

	def onLoseFocus(self):
		self.tempArrow = self.arrow
		self.arrow = ""
		self.redraw()
	
	def onFocus(self):
		if self.tempArrow is not "":
			self.arrow = self.tempArrow
			self.tempArrow = ""
			self.redraw()
	
	def __init__(
		self, 
		parent, 
		positionYX, 
		sizeYX, 
		options, 
		maxSelect=-1, 
		title='Select', 
		arrow=" =>",
		footer="Space = toggle, Enter = accept, q = cancel",
		more="...",
		border="||--++++",
		c_selected="[X]",
		c_empty="[ ]"
	):
		self.title = title
		self.arrow = arrow
		self.footer = footer
		self.more = more
		self.border = border
		self.c_selected = c_selected
		self.c_empty = c_empty
		self.window_height = sizeYX[0]
		self.window_width = sizeYX[1]
		self.maxSelect = maxSelect
		
		self.all_options = []
		
		for option in options:
			self.all_options.append({
				"label": option,
				"selected": False
			})
			self.length = len(self.all_options)
		
		# Set up window.
		self.win = parent.derwin(
			sizeYX[0],
			sizeYX[1],
			positionYX[0],
			positionYX[1]
		)
		self.onInput(-1)
