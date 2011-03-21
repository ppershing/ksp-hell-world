#!/usr/bin/python

import re
import os
import gtk
import glib
import webkit
import signal
import os.path
import gobject
import threading
log_path = './log.html'
tasks_path = '../testovac/tasks/'
done_dir = './done/'
saves_dir = './saves/'
last_update = 0
n_choices = 2
witch_timeout =10*60*1000
#witch_timeout =10*1000

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

gtk.threads_init ()

def launch_editor (task, lang):
	gobject.idle_add (tc_window.hide_all)
	quit = False
	while not quit:
		quit = True
		if lang == 'HellC':
			ext ='.hellc'
		elif lang == 'HellP':
			ext = '.hellp'
		file_path = os.path.join(saves_dir, task + ext)
		ret = os.system ('./editor.py %s' % file_path)
		ret = ret >> 8
		print "got "+str(ret)
		if False: pass
		elif ret == 0:
			# Normal exit
			pass
		elif ret == 47:
			# Solution was accepted 
			os.system ("touch '%s'" % os.path.join (done_dir, task))
		elif ret == 74:
			# expected failure, return quietly as if it was 0
			pass
		else:
			# crash ? Try reloading last state
			quit = False
	gobject.idle_add (tc_window_restore)
		
def tc_window_restore(*args):
	update_task_buttons ()
	tc_window.show_all ()
	tc_window.move (0, 0)

def refresh_log ():
	log = open (log_path).read()
	if log.find('<body') == -1:
		log = '<body bgcolor="black" style="color: white">' + log + '</body>'
		log = log.replace (chr(10), '<br/>')
	log_webkit.load_html_string (log,base_uri='.')

def update_view ():
	global last_update

	# test change of logfile
	try:
		current_update = os.stat (log_path).st_mtime

		if last_update < current_update:
			last_update = current_update
			refresh_log ()
	except OSError:
		pass
	return True

def get_available_tasks ():
	available_tasks = task_list
	solved_tasks = filter (is_task, map(os.path.basename,	os.listdir(done_dir)))

	for task in solved_tasks:
		if task in available_tasks:
			available_tasks.remove (task)
	
	return available_tasks[0:n_choices]

def is_task (x):
	return re.match (r'^[0-9][0-9].*$', x) != None

def update_task_buttons ():
	current_tasks = get_available_tasks ()
	for i in range(0, n_choices):
		tc_tasks[i].set_label (current_tasks[i])


def task_selected (sender):
	update_task_buttons ()
	selected_task = sender.get_label()
	selected_language = tc_language.get_active_text()
	task_desc = open (os.path.join (tasks_path, selected_task, 'desc')).read()
	task_desc ='<body bgcolor="black" style="color: red">'+task_desc+'</body>'
	task_webkit.load_html_string (task_desc, base_uri= '.')
	file(log_path,'w+').write('')

	print selected_task, selected_language 
	threading.Thread (target = launch_editor, args = (selected_task, selected_language)).start()

try:
	os.unlink (log_path)
except:
	pass


def witch_screen (show):
	if show:
		witch.show_all ()
		glib.timeout_add (2000, witch_screen, False)
	else:
		witch.hide_all ()
		glib.timeout_add (witch_timeout, witch_screen, True)
	return False


# load current state

task_list = filter(is_task, map(os.path.basename, os.listdir(tasks_path)))
task_list.sort ()

print get_available_tasks ()

# log window
log_window = gtk.Window ()
log_scrollarea = gtk.ScrolledWindow ()
log_webkit = webkit.WebView ()
log_scrollarea.add (log_webkit)
log_window.add (log_scrollarea)

# Now, find out dimensions of the screen; assuming we run on one screen
screen = log_window.get_screen ()
width = screen.get_width ()
height = screen.get_height ()

# task description window
task_window = gtk.Window ()
task_scrollarea = gtk.ScrolledWindow ()
task_webkit = webkit.WebView ()
task_scrollarea.add (task_webkit)
task_window.add (task_scrollarea)

# task choice window
tc_language = gtk.combo_box_new_text ()

langs = ['HellC', 'HellP']
for i in langs:
	#it = options.append ()
	#options.set (it, 0, i)
	tc_language.append_text (i)
tc_language.set_active (0)

tc_window = gtk.Window ()
tc_vbox = gtk.VBox (homogeneous = False)
tc_vbox.set_homogeneous (False)
tc_tasks = []
for i in range (0, n_choices):
	tc_tasks += [ gtk.Button() ]
	vbox = gtk.VBox ()
	tc_tasks[-1].connect ('clicked', task_selected)

tc_vbox.pack_start (tc_language, expand = False)
tc_btnbox = gtk.HBox ()
for i in tc_tasks: tc_btnbox.add (i)
tc_vbox.pack_start (tc_btnbox)
tc_window.add (tc_vbox)

# Bonus, witch window
witch = gtk.Window()
witch_box = gtk.HBox ()
witch_img = gtk.Image ()
witch_box.add (witch_img)
witch.add (witch_box)
witch.fullscreen ()
witch_pixbuf = gtk.gdk.Pixbuf (gtk.gdk.COLORSPACE_RGB, True, 8, width, height)
witch_original = gtk.gdk.pixbuf_new_from_file ('images/bosorka.png')
witch_original.copy_area (0, 0, 
		min(witch_original.get_width (), width),
		min(witch_original.get_height (), height),
		witch_pixbuf, 0, 0)
witch_img.set_from_pixbuf (witch_pixbuf)
witch.set_deletable (False)

log_window.show_all ()
task_window.show_all ()
tc_window.show_all ()

update_task_buttons ()

log_window.move (5, 520)
task_window.move (640+10, 0)
tc_window.move (0,0)

log_window.resize (width-5, height-520)
task_window.resize (width-640 -10, 480)
tc_window.resize (640,480)

glib.timeout_add (100, update_view)
glib.timeout_add (witch_timeout, witch_screen, True)
log_window.connect ('destroy', gtk.main_quit)
task_window.connect ('destroy', gtk.main_quit)
tc_window.connect ('destroy', gtk.main_quit )

gtk.main()
