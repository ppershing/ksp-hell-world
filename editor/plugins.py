from abc import abstractmethod
from view import *
from random import *

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
	
	dest.blit (src, (x, y), area = tuple(area))


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

	def disown (self, view, blockno, line):
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
		text = wp.font.render (block.text, 0, (randint(128, 255), randint (64, 96), randint(64, 96)) )
		pygame.draw.rect(text, (0, 0, 0), (0, 0, text.get_width() - 1, self.burnt))
		blit_clipped (wp.screen, text, rect)

		# tick

		self.burnt += 0.2
		if self.burnt >= text.get_height():
			block.text = '.'*len(block.text)
			self.disown (view, blockno, line)

class HelloWorld(WordMatchPlugin):
	my_string = 'Hello, world'
	
	def __init__ (self):
		self.anim_time = -200  # animation time, 0 -- 100
	
	
	def delete (self, view, blockno, line, offset, char):
		self.disown (view, blockno, line)

	def insert (self, view, blockno, line, offset):
		self.disown (view, blockno, line)

	def render (self,view, blockno, line, wp, rect):
		
		if self.anim_time < 254:
			self.anim_time += 2
		else: self.anim_time = 255	
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
