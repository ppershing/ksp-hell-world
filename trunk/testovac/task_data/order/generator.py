#!/usr/bin/python
import random;

s=set()

def inwrite():
    global s;
    x=0;
    while (x in s):
        x=random.randint(0, 1000000)
    s.add(x)
    print x


def inorder_walk(n):
    if (n==0):
        print "("
        print ")"
        return
    n1 = int(n*w);
    n2 = n - n1 - 1
    print "("
    if (random.randint(0,1)):
        inorder_walk(n1)
        inwrite();
        inorder_walk(n2)
    else:
        inorder_walk(n2)
        inwrite();
        inorder_walk(n1)
    print ")"

n=input() #"zadaj pocet vrcholov:")
w=input() #"zadaj vyvazenost generovania:");
inorder_walk(n)
