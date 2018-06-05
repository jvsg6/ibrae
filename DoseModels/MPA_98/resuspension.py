#!/usr/bin/python2.7
# -*- coding: utf-8 -
import sys
import os
from os import path
from math import exp
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from AdditionalFunctions.createGraph import createGraph


def calcK(t, l):
	K1 = 1e-5
	K2 = 1e-9
	l1 = 1.46e-7
	l2 = 2.2e-10
	return t

def main():
	x = [i for i in range(0, 31536001, 10000)]
	print len(x)
	y = []
	for t in x:
		y.append(calcK(t, 1))
	createGraph(x, y, "first.png", False)
	print "Done!!!"
	return

if __name__=="__main__":
	sys.exit(main())