from abc import abstractmethod
from view import *
from random import *
from pygame.mixer import Sound
import pygame.mixer

def blit_clipped (dest, src, (x, y, w, h) ):
	area = [0, 0, src.get_width(), src.get_height()]

	if x < 0:
		area[0] -= x
		area[2] -= x
		x=0
	
	if y < 0:
		area[1] -= y
		area[3] -= y
		y=0
	
	dest.blit (src, (x, y), tuple(area))


class Plugin:
	@abstractmethod
	def insert (self, view, blockno, line, offset):
		"""
		Called when a character in bound block is inserted
		"""
		pass

	@abstractmethod
	def delete (self, view, blockno, line, offset, deleted_char):
		"""
		Called when a characted in bound block is deleted
		"""
		pass

	@classmethod
	@abstractmethod
	def updated_unbound_block (self, view, blockno, line):
		"""
		Called when unbound block is changed 
		"""
		pass

	@abstractmethod
	def render (self, view, blockno, line, viewport, rect):
		pass

	@abstractmethod 
	def move_cursor (self, oldpos, delta):
		"""
		Called when cursor moves in bound block
		"""
		pass

	def disown (self, view, blockno, line):
		print view.lines
		print blockno, line
		view.lines[line][blockno].manager = None
		view.new_block (blockno, line)

class WordMatchPlugin(Plugin):
	@classmethod
	def updated_unbound_block (cls, view, blockno, line):
		block = view.lines[line][blockno]
		
		pos = block.text.find(cls.my_string)
		if pos == -1:
			return False
		
		# Split block into my new block, two remaining blocks 
		replacement = filter (lambda x: x.text != '', [block [0:pos], Block(cls.my_string, cls()), block[pos + len(cls.my_string):]])

		view.lines[line] = view.lines[line][0:blockno] + replacement + view.lines[line][blockno+1:]
		if block[0:pos].text != '':
			view.new_block(blockno, line)

		if block[pos + len(cls.my_string):].text != '':
			add = 1
			if len(replacement)>2:
				add = 2
			view.new_block(blockno + add, line)
		return True


class Burn(WordMatchPlugin):
	my_string = 'burn'
	def __init__ (self):
		self.burnt = 0

	def delete (self, view, blockno, line, offset, char):
		self.disown (view, blockno, line)

	def insert (self, view, blockno, line, offset):
		self.disown (view, blockno, line)

	def render (self,view, blockno, line, wp, rect):
		block = view.lines[line][blockno]
		c = (float(self.burnt)/float(wp.char_height))*64
		text = wp.font.render (block.text, 0, (randint(128, 255) - c , randint (64, 96) - c , randint(64, 96) - c) )
		pygame.draw.rect(text, (0, 0, 0), (0, 0, text.get_width() - 1, self.burnt))
		blit_clipped (wp.screen, text, rect)

		# tick

		self.burnt += 0.1
		if self.burnt >= text.get_height():
			block.text = '.'*len(block.text)
			self.disown (view, blockno, line)

class HelloWorld(WordMatchPlugin):
	my_string = 'Hello, world'
	
	def __init__ (self):
		self.anim_time = -200  # animation time, 0 -- 100
	
	
	def delete (self, view, blockno, line, offset, char):
		block = view.lines[line][blockno]
		if block.text == '' or self.anim_time > 254 or self.anim_time <0:
			self.disown (view, blockno, line)

	def insert (self, view, blockno, line, offset):
		if self.anim_time > 254 or self.anim_time < 0:
			self.disown (view, blockno, line)

	def tick (self, view, blockno, line, wp):
		if self.anim_time < 254:
			self.anim_time += 2
		else: self.anim_time = 255	
	
	def render (self, view, blockno, line, wp, rect):
		self.tick (view, blockno, line, wp)		

		c = max (0, self.anim_time)

		color = (255, 255 - c, 255 - c)
		block = view.lines[line][blockno]
		text = wp.font.render (block.text, 0, color )
		blit_clipped (wp.screen, text, rect)
		
		if self.anim_time < 0:
			return

		if self.anim_time <= 254:
			block.text = 'Hell   world'
			ocomma = wp.font.render ('o,', 0, (255- self.anim_time, 255-self.anim_time, 255-self.anim_time))
			ocomma_rect = (rect[0]+wp.char_width*4, rect[1]+self.anim_time/2, rect[2], rect[3])
			blit_clipped (wp.screen, ocomma, ocomma_rect)

class Trap(WordMatchPlugin):
	my_string = 'trap'

	def __init__ (self):
		self.momentum = 0
		self.yoffset = 0
		self.direction = 1.2
	
	def delete (self, view, blockno, line, offset, char):
		self.disown(view, blockno, line)
	
	def insert (self, view, blockno, line, offset):
		self.disown(view, blockno, line)

	def move_cursor (self, oldpos, delta):
		if delta[1] != 0:
			self.momentum += 6
		else:
			self.momentum += 4

	def tick (self, view, blockno, line, wp):
		if (self.momentum == 0) and (self.yoffset == 0):
			return True

		self.yoffset += self.direction 

		# returning to normal position
		if self.yoffset <= 0:
			self.yoffset = 0
			self.momentum /= 2
			self.direction =- self.direction
		
		# if we have not reached critical momentum, switch direction and
		# return
		if self.yoffset > self.momentum and self.momentum < 12:
			self.direction = -self.direction
		else:
			# critical momentum reached, fall on the line below
			if self.yoffset < wp.char_height:
				return True

			# make the letters fall one line below

			# if there's no line, create one
			if len(view.lines) <= line+1:
				view.lines += [[Block('', None)]]

			# pad line to the position below us
			block_start = view.get_coord_from_block_offset(blockno,line)

			view.lines[line+1][-1].text += ' '*(len(self.my_string) + block_start - view.line_length(line+1))
			for i in range(0, len(self.my_string)):
				view.insert (self.my_string[i], block_start + i, line + 1)
				view.delete (1, block_start + i + 1, line + 1)
			view.lines[line][blockno].text = ' '*len(self.my_string)
			self.disown(view, blockno, line)

			view.move_cursor (0, 1)
			return False
		return True
			

	def render (self, view, blockno, line, wp, rect):
		if not self.tick (view, blockno, line, wp):
			return

		block = view.lines[line][blockno]
		color = (0, 0, 255)
		text = wp.font.render (block.text, 0, color)
		myrect = (rect[0], rect[1] + self.yoffset, rect[2], rect[3])
		blit_clipped (wp.screen, text, myrect)
		
class StaticWordHighlight(Plugin):
	word_colors = {
			'bloody': { 'color': (255, 0, 0),'sound': Sound ('sounds/bloody.wav') },
		'#brains': { 'color': (0, 255, 0), }
	}

	def __init__ (self, word):
		self.word = word

	@classmethod
	def updated_unbound_block (cls, view, blockno, line):
		block = view.lines[line][blockno]
		
		pos = -1
		for word in cls.word_colors:

			pos = block.text.find(word)
			if pos == -1:
				continue
			
			# Split block into my new block, two remaining blocks 
			replacement = filter (lambda x: x.text != '', [block [0:pos], Block(word, cls(word)), block[pos + len(word):]])

			view.lines[line] = view.lines[line][0:blockno] + replacement + view.lines[line][blockno+1:]
			if block[0:pos].text != '':
				view.new_block(blockno, line)

			if block[pos + len(word):].text != '':
				add = 1
				if len(replacement)>2:
					add = 2
				view.new_block(blockno + add, line)
		if (pos == -1):
			return False
		return True
	def move_cursor (self, oldpos, delta):
		me = self.word_colors[self.word]
		if not me.has_key('sound'):
			return
			
		me['sound'].stop ()
		me['sound'].play ()

	def delete (self, view, blockno, line, offset, char):
		self.disown (view, blockno, line)

	def insert (self, view, blockno, line, offset):
		self.disown (view, blockno, line)

	def render (self,view, blockno, line, wp, rect):
		block = view.lines[line][blockno]
		text = wp.font.render (block.text, 0, self.word_colors[self.word]['color'] )
		blit_clipped (wp.screen, text, rect)
