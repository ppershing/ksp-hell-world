import pygame

class Block:
	def __init__ (self, text, manager):
		self.text = text
		self.manager = manager
	
	def __getslice__ (self, a, b):
		return Block (self.text[a:b], self.manager)

	def __getitem__ (self, a):
		return self.text[a]

	def __add__ (self, a):
		try:
			return self._add_left (a)
		except NotImplementedError:
			try:
				return a._add_right (self)
			except:
				raise NotImplementedError
		return

	def __radd__ (self, a):
		try:
			return self._add_right (a)
		except NotImplementedError:
			try:
				return a._add_left (self)
			except:
				raise NotImplementedError
		return
	def _add_left (self, a):
		if isinstance(a, str) or isinstance(a, unicode):
			return Block(self.text + a, self.manager)
		elif isinstance(a, Block):
			if a.manager != self.manager:
				raise NotImplementedError('Incompatible managers')
			return Block (self.text + a. text, self.manager)
		else:
			raise NotImplementedError('Cannot add %s and %s' % (type(self), type(a)))
	def _add_right (self, a):
		if isinstance(a, str) or isinstance(a, unicode):
			return Block(a + self.text, self.manager)
		elif isinstance(a, Block):
			if a.manager != self.manager:
				raise NotImplementedError('Incompatible managers')
			return Block (a.text+self.text, self.manager)
		else:
			raise NotImplementedError('Cannot add %s and %s' % (type(self), type(a)))

	def __repr__ (self):
		return "('%s', %s)" % (self.text, repr(self.manager))
	def __str__ (self):
		return self.text

class Viewport:
	def __init__ (self, width, height):
		self.screen = pygame.display.set_mode ((width, height))
		self.font = pygame.font.SysFont ('monospace', 16)
		(self.char_width, self.char_height) = self.font.size ('I')
		


class ViewData:
	def __init__ (self, width, height):
		self.offset = [0,0]
		self.lines = [[Block(u'testing', None), Block(u' another', None) ]]
		self.cursor = [0,0]
		self.plugins = []
		self.width = width
		self.height = height

	def __str__ (self):
		ret = ''.join([''.join(map(lambda s: str(s), x)+ [ '\n' ]) for x in self.lines])
		return ret

	def line_length (self, line):
		return sum (len (x.text) for x in self.lines[line])

	def get_line (self, line):
		return ''.join([x.text for x in self.lines[line]])

	def move_cursor (self, dx, dy):
		"""
		Moves cursor relatively to specified coords
		"""
		
		oldpos = self.cursor
		(blockno, blockoffset)  = self.get_block_offset (self.cursor[0], self.cursor[1])
		oldblock = self.lines[self.cursor[1]][blockno]
		
		if dy < 0:
			if self.cursor[1] > 0:
				self.cursor[1] += dy
			if self.cursor[1] - self.offset[1] < 0:
				self.offset[1] += self.cursor[1] - self.offset[1]

		if dy > 0:
			if self.cursor[1] < len(self.lines) - 1:
				self.cursor[1] += dy
			if self.cursor[1] - self.offset[1] >= self.height:
				self.offset[1] += self.cursor[1] - self.offset[1] - self.height

		# Check whether we are still in bounds of a line
		if self.cursor[0] > self.line_length (self.cursor[1]):
			dx = -(self.cursor[0] - self.line_length (self.cursor[1]))
		
		
		if dx < 0:
			if self.cursor[0] > 0:
				self.cursor[0] += dx
			if self.cursor[0] - self.offset[0] < 0:
				self.offset[0] += self.cursor[0] - self.offset[0]
		if dx > 0:
			if self.cursor[0] < sum([len(x.text) for x in self.lines[self.cursor[1]]]):
				self.cursor[0] += dx
			if self.cursor[0] - self.offset[0] >= self.width:
				self.offset[0] += self.cursor[0] - self.offset[0] - self.width
		
		(blockno, blockoffset)  = self.get_block_offset (self.cursor[0], self.cursor[1])
		newblock = self.lines[self.cursor[1]][blockno]

		if oldblock.manager is not None:
			oldblock.manager.move_cursor (oldpos, (dx, dy))
		
		if newblock.manager is not None:
			newblock.manager.move_cursor (oldpos, (dx, dy))


	
	def get_block_offset (self, x, y):
		"""
		For given coordinates, returns block and offset containing specified character.
		"""
		line = self.lines[y]
		my_x = 0

		for i in range (0, len(line)):
			block = line[i]
			if (x >= my_x) and (x < my_x + len(block.text)):
				return (i, x - my_x)
			my_x += len(block.text)
		if my_x == self.line_length (y):
			lastblock = self.lines[y][-1]
			return (len(self.lines[y])-1, len(lastblock.text))

		return None

	def get_coord_from_block_offset (self, blockno, line, offset=0):
		assert line < len (self.lines)
		assert blockno < len (self.lines[line])
		assert offset < len(self.lines[line][blockno].text) or offset == 0

		ret = 0

		for i in self.lines[line][0:blockno]:
			ret += len (i.text)
		ret += offset

		return ret

	def break_line (self, x = None, y = None):
		"""
		Breaks line into two lines at given position
		"""
		if x is None:
			x = self.cursor[0]
		if y is None:
			y = self.cursor[1]
		line = self.lines[y]
		(blockno, blockoffset) = self.get_block_offset (x, y)
		block = line[blockno]
		# insert a new line

		# generate two new lines
		oldline = line[0:blockno] + [block[0:blockoffset]]
		newline = [block[blockoffset:]] + line [blockno+1:] 
		
		# ... and insert them into the model
		self.lines[y] = oldline
		self.lines.insert(y+1, newline)
		# EVENT new blockat the end of oldline and start of newline

		self.new_block(blockno, y)
		self.new_block(0, y+1)

	def insert (self, c, x = None, y = None):
		if x is None:
			x = self.cursor[0]
		if y is None:
			y = self.cursor[1]
		
		line = self.lines[y]
		(blockno, blockoffset) = self.get_block_offset (x, y)
		block = line[blockno]
	
		# insert new letter to the block
		newblock = block[0:blockoffset] + c + block[blockoffset:]
		self.lines[y][blockno] = newblock
		
		## EVENT
		
		if block.manager == None:
			for plugin in self.plugins:
				if plugin.updated_unbound_block (self, blockno, y):
					break
		else:
			block.manager.insert (self, blockno, y, blockoffset)

	def delete_newline (self, y = None):
		if y is None:
			y = self.cursor[1]
		
		# Don't ever delete the last line
		if (len(self.lines) == 1):
			return

		# neither delete nonexisting line
		if (y >= len (self.lines)-1):
			return


		#we are going to delete line
		if y == -1:
			return
		old_length = len(self.lines[y])
		self.lines[y] += self.lines[y+1]
		del self.lines[y+1]

		# Update blocks
		if old_length < len (self.lines[y]):
			self.new_block (old_length, y)
			self.new_block (old_length-1, y)

	def delete (self, count = 1, x = None, y = None):
		if x is None:
			x = self.cursor[0]
		if y is None:
			y = self.cursor[1]
		line = self.lines[y]
		deleted = False

		# don't delete last block

		assert x >= 0
		#delete a character
		(blockno, blockoffset) = self.get_block_offset (x, y)
		block = line[blockno]
		deleted_char = block[blockoffset]
		newblock = block[0:blockoffset] +  block[blockoffset+count:]
		
		if newblock.text != '':
			self.lines[y][blockno] = newblock
		else:
			if (len(self.lines) != 1) and (len(self.lines[y]) != 1):
				del self.lines[y][blockno]
				deleted = True
			else:
				self.lines[y][blockno] = newblock
		
		if block.manager == None:
			if not deleted:
				for plugin in self.plugins:
					if plugin.updated_unbound_block (self, blockno, y):
						break
		else:
			block.manager.delete (self, blockno, y, blockoffset, deleted_char)


		## EVENT
	def new_block (self, blockno, line):
		# try merging blocks
		block = self.lines[line][blockno]
		
		for i in [0, -1]:
			if (blockno+i) < 0 or (blockno+i+1) >= len(self.lines[line]):
				continue

			neighbor = self.lines[line][blockno+i]
			try:
				newblock = self.lines[line][blockno+i] + self.lines[line][blockno+i+1]
				if newblock != None:
					self.lines[line][blockno+i] = newblock
					del self.lines[line][blockno+i+1]
					if i == -1:
						blockno -= 1 # Block has moved one position to the left
			except NotImplementedError:
				pass
		if block.manager == None:
			for plugin in self.plugins:
				if plugin.updated_unbound_block (self, blockno, line):
					break
		else:
			block.manager.disown (self, blockno, line)


			

		
