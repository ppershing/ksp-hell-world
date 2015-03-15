# How to install #

### What you will need: ###
> python
> python-pygtk
> python-pygame
> mplayer

### How to install: ###
  * First of all, if you are on windows, you can enjoy the editor itself, but you can't use tester, try to get a linux machine if you want to test your code.
  * download Hell world from svn repository or as a zip file
  * `cd testovac`
  * Compile wrapper for testing: "`gcc wrapper-mj-amd64.c -o wrapper`" or "`gcc wrapper-mj-x86.c -o wrapper`" depending on your architecture
  * `cd ../soundtrack`
  * `mplayer -volume 20 -softvol -loop 0 -shuffle *.mp3`
  * `cd ../editor`
  * `./editor-master.py`

### How to remove backups: ###

Editor backups each test/compilation and you may soon run out of disk, erase everything in directory testovac/sandbox (but not the directory itself)


### How to reset solved tasks: ###

Remove `editor/done/*` and  `editor/saves/*`