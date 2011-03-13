#!/usr/bin/python
import sys
from random import randint

if len(sys.argv) == 1:
	print "Usage: generator.py amount [min=1 [max=10000000]]"

else:
	amount = int(sys.argv[1])
	min = 1
	if len(sys.argv)>2: min = int(sys.argv[2]) 
	max = 10000000
	if len(sys.argv)>3: max = int(sys.argv[3])

	print amount
	for i in range(amount): print randint(min, max),
	print
