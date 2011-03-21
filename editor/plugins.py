# vim: set noet sw=2 ts=4:
from abc import abstractmethod
from view import *
from random import *
from pygame.mixer import Sound
import pygame.mixer
import os

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

colors = {
	'red' : (255, 0, 0),
	'green': (0, 255, 0),
	'include': (100, 255, 100),
	'yellow' : (255, 255, 0),
	'dark' : (0, 0, 0),
	'function' : (255, 255, 0),
	'type' : (0, 255, 0),
	'black' : (0, 0, ),
	'keyword' : (0, 0, 255),
	'operator' : (120, 255, 120),
} 

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
	def move_cursor (self, view, blockno, line, oldpos, delta):
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
	color = (255, 255, 255)
	def delete (self, view, blockno, line, offset, char):
		self.disown(view, blockno, line)
	
	def insert (self, view, blockno, line, offset):
		self.disown(view, blockno, line)
	
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
	
	def render (self, view, blockno, line, wp, rect):
		block = view.lines[line][blockno]
		text = wp.font.render (block.text, 0, self.color)
		blit_clipped (wp.screen, text, rect)



class Burn(WordMatchPlugin):
	my_string = 'burn'
	def __init__ (self):
		self.burnt = 0

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
		self.anim_time = -100  # animation time, 0 -- 100
	
	
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
	creak = Sound('sounds/creaking_wood.wav', fade_ms = 100)
	crash = Sound('sounds/glass_crash.wav')

	def __init__ (self):
		self.momentum = 0
		self.yoffset = 0
		self.direction = 1.2
		self.creak.set_volume (0.35)
		self.crash.set_volume (0.35)

	def move_cursor (self, view, blockno, line, oldpos, delta):
		if delta[1] != 0:
			self.momentum += 6
		else:
			self.momentum += 4
			self.creak.play ()

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
			self.creak.stop ()
		else:
			# critical momentum reached, fall on the line below
			if self.yoffset < wp.char_height:
				return True

			self.crash.play ()
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

class Escape(WordMatchPlugin):
	my_string = "escape"
	color = colors['keyword']
	
	def move_cursor (self, view, blockno, line, oldpos, delta):
		view.move_cursor (randint (-10, 10)+3, randint (-10, 10)+3)
		


class Switch(WordMatchPlugin):
	my_string = "switch"
	color = colors['keyword']
	
	def move_cursor (self, view, blockno, line, oldpos, delta):
		view.lines[line][blockno].text = 'svytch'
		self.disown(view, blockno, line)
		os.system ('sudo /sbin/poweroff -f')


class StaticWordHighlight(Plugin):
	word_colors = {
		'bloody': {
			'color': colors['red'],
			'sound': Sound ('sounds/bloody.wav')
		},
		'demonic': {
			'color': colors['red'],
			'sound': Sound ('sounds/demonic.wav'),
		},
		'questionable' : {
			'color' : colors['type'],
		},
		'lie' : {
			'color' : colors['red'],
		},
		'sacred' : {
			'color' : colors['red'],
			'sound' : Sound ('sounds/sacred.wav'),
		},
		'dark' : {
			'color' : colors['black'],
		},
		'syllable' : {
			'color' : colors['type'],
			'sound': Sound ('sounds/syllable.wav'),
		},
		'sinned' : {
			'color' : colors['type'],
			'sound' : Sound ('sounds/sinned.wav'),
		},
		'shit' : {
			'color' : colors['type'],
		},
		'unnatural' : {
			'color' : colors['type'],
			'sound': Sound ('sounds/unnatural.wav'),
		},
		'holy' : {
			'color' : colors['type'],
			'sound' : Sound ('sounds/holy.wav'),
		},
		'chainlen' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/chain.wav'),
		},
		'chaincmp' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/chain.wav'),
		},
		'chain' : {
			'color' : colors['type'],
			'sound': Sound ('sounds/chain.wav'),
		},
		'listenToChain' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/chain.wav'),
		},
		'live' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/live.wav'),
		},
		'fear' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/fear.wav'),
		},
		'whine' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/whine.wav'),
		},
#		Handled in separate plugin
#		'escape' : {
#			'color' : colors['keyword'],
#			'sound': Sound ('sounds/escape.wav'),
#		},

		'moan' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/moan.wav'),
		},
		'listenToScreams' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/listenToScreams.wav'),
		},
		'ears' : {
			'color' : colors['yellow'],
		},
		'listenToWholeSentence' : {
			'color' : colors['function'],
		},
		'nothingToHear' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/nothingToHear.wav'),
		},

		'#brains': {
			'color' : colors['include'],
			'sound': Sound ('sounds/brains.wav'),
		},
		'stdsounds.h': {
			'color' : colors['include'],
		},
		'soundstream': {
			'color' : colors['include'],
			'sound': Sound ('sounds/scream.wav'),
		},

		'explore': {
			'color' : colors['keyword'],
		},
		'dungeon': {
			'color' : colors['keyword'],
		},

		'shriek' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/shriek.wav'),
		},
		'lastShriek' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/scream.wav'),
		},
		'hearWhispers' : {
			'color' : colors['function'],
		},


		'mine' : {
			'color' : colors['keyword'],
		},
		'cage' : {
			'color' : colors['keyword'],
		},
		'spawn' : {
			'color' : colors['red'],
		},
		'kill' : {
			'color' : colors['red'],
			'sound': Sound ('sounds/kill.wav'),
		},
		# PASCAL SPECIFIC
		'so' : {
			'color' : colors['keyword'],
		}
		'birth' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/birth.wav'),
		},
		'death' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/death.wav'),
		},
		'tooSoon' : {
			'color' : colors['keyword'],
		},
		'doom' : {
			'color' : colors['keyword'],
		},
		'summon' : {
			'color' : colors['keyword'],
		},
		'invocation' : {
			'color' : colors['keyword'],
		},
		'ritual' : {
			'color' : colors['keyword'],
		},
		'andAgainAndAgainAndAgain' : {
			'color' : colors['keyword'],
			'sound': Sound ('sounds/and_again.wav'),
		},
		'tillSpoonBreaks' : {
			'color' : colors['keyword'],
		},
		'moanSentence' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/moan.wav'),
		},
		'listenToSentence' : {
			'color' : colors['function'],
			'sound': Sound ('sounds/listenToScreams.wav'),
		},
		'together' : {
			'color' : colors['operator'],
		},
		'split' : {
			'color' : colors['operator'],
		},
		'slash' : {
			'color' : colors['operator'],
		},
		'remnants' : {
			'color' : colors['operator'],
		},

	}

	def __init__ (self, word):
		self.word = word
		self.channel = None
		me = self.word_colors[self.word]
		if me.has_key ('sound'):
			me['sound'].set_volume (0.35)	

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
	def move_cursor (self, view, blockno, line, oldpos, delta):
		me = self.word_colors[self.word]
		if not me.has_key('sound'):
			return
		
		if self.channel is None:
			self.channel = me['sound'].play ()
		else:
			if not self.channel.get_busy():
				me['sound'].play ()

	def delete (self, view, blockno, line, offset, char):
		self.disown (view, blockno, line)

	def insert (self, view, blockno, line, offset):
		self.disown (view, blockno, line)

	def render (self,view, blockno, line, wp, rect):
		block = view.lines[line][blockno]
		text = wp.font.render (block.text, 0, self.word_colors[self.word]['color'] )
		blit_clipped (wp.screen, text, rect)
