#!/usr/bin/python
import sys
from random import choice
from string import ascii_lowercase

if len(sys.argv) == 1:
	print "Usage: generator.string.py length"

else:
	amount = int(sys.argv[1])
	#print amount
	for i in range(amount): sys.stdout.write(choice(ascii_lowercase))
	print
