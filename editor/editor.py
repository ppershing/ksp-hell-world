#!/usr/bin/python
import string
import pygame
import sys
import os
import re

pygame.init ()
pygame.mixer.init ()

from pygame.locals import *
from plugins import *
from view import *

def save (view):
	open(file_path, 'w+').write(str(view))

def run_test (view):
	save (view)
	ret = os.system ('sh ../testovac/testovac.sh %s %s >log.html' % (file_path, task, ))
	print "Tester returned "+ str(ret)
	if ret == 0:
		# we are done
		#pygame.quit ()
		sys.exit (1)

if len(sys.argv) >1:
	file_path = sys.argv[1]
else:
	file_path = 'test.hellc'

file_name = os.path.basename (file_path)
m = re.match ("^(.*)\.([a-z]+)$", file_name)
if m == None:
	print "could not parse file name: " + file_name
	sys.exit (47)
language = m.group(2)
task = m.group(1)
print task, language


### main

pygame.key.set_repeat (200, 25)
pygame.display.set_caption (file_name)
wp = Viewport (640, 480)
clock = pygame.time.Clock ()
max_width = wp.screen.get_width()/wp.char_width
max_height = wp.screen.get_height()/wp.char_height

try:
	content = map (string.rstrip, file (file_path).readlines ())
except:
	content = ['']

view = ViewData (max_width, max_height)

view.plugins.append(Burn)
view.plugins.append(HelloWorld)
view.plugins.append(Trap)
view.plugins.append(Escape)
view.plugins.append(StaticWordHighlight)
view.set_content (content)

open("log.html","w+").write('')

while 1:
	clock.tick (25)
	x = 0
	y = 0
	wp.screen.fill ((0,0,0))
	for lineno in range (0, len(view.lines [view.offset[1]:])):
		line = view.lines[view.offset[1] + lineno]
		data_x = 0
		for blockno in range (0, len(line)):

			if blockno >= len(line):
				# we need this because some actions do in-place 
				# modifications to blocks, and even telete them
				break
			elem = line[blockno]
			to_print = elem.text[
				max(view.offset[0] - data_x ,0):
				max(view.offset[0] - data_x, 0) +
					len(elem.text)]

			# FIXME: text width bigger than screen
			if elem.manager is None:
				text = wp.font.render ( to_print, 0, (255,255,255))
				wp.screen.blit (text, (x*wp.char_width, y*wp.char_height))
			else:
				elem.manager.render (view, blockno, lineno, wp, 
					((data_x-view.offset[0])*wp.char_width, y*wp.char_height, wp.char_width* len(to_print), wp.char_height) )
			x += len (to_print)
			data_x += len(elem.text)
		x = 0
		y += 1

	# cursor
	cursor_disp_x = view.cursor[0] - view.offset[0]
	cursor_disp_y = view.cursor[1] - view.offset[1]
	pygame.draw.line (wp.screen, (255, 255, 255),
		(cursor_disp_x*wp.char_width, cursor_disp_y*wp.char_height),
		(cursor_disp_x*wp.char_width, (cursor_disp_y+1)*wp.char_height - 1))

	pygame.display.flip()


	# Process events
	for event in pygame.event.get ():
		if event.type == QUIT:
			save (view)
			sys.exit (0)
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				save (view)
				sys.exit (0)
			elif event.key == K_F5:
				run_test (view)
			elif event.key == K_UP:
				view.move_cursor (0, -1)
			elif event.key == K_DOWN:
				view.move_cursor (0, 1)
			elif event.key == K_LEFT:
				view.move_cursor (-1, 0)
			elif event.key == K_RIGHT:
				view.move_cursor (1, 0)
			elif event.key == K_HOME:
				view.move_cursor (-view.cursor[0], 0)
			elif event.key == K_END:
				view.move_cursor (view.line_length(view.cursor[1]) - view.cursor[0], 0)
			elif event.key == K_TAB:
				tabsize = 4
				for i in range (0,tabsize):
					view.insert(' ')
				view.move_cursor(tabsize, 0)
			elif event.key == K_DELETE:
				if view.cursor[0] < view.line_length (view.cursor[1]):
					view.delete ()
				else:
					view.delete_newline ()
			elif event.key == K_BACKSPACE:
				if view.cursor[0] > 0:
					#delete a char
					view.move_cursor (-1, 0)
					view.delete ()

				else:
					#delete newline
					if view.cursor[1] > 0:
						newpos = view.line_length (view.cursor[1]-1)
						view.move_cursor(newpos-view.cursor[0], -1)
						view.delete_newline(view.cursor[1])

			elif event.key == K_RETURN:
				view.break_line ()
				view.move_cursor(0, 1)
				view.move_cursor(-view.cursor[0], 0)
			else:
				if (len(event.unicode) == 1):
					view.insert (event.unicode)
					view.move_cursor(1, 0)
			print view.lines

