#!/usr/bin/python2.7
# -*- coding: utf-8 -
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams
    
    
def save(name='', fmt='png'):
	pwd = os.getcwd()
	iPath = './pictures/{}'.format(fmt)
	try:
		os.makedirs(iPath)
	except WindowsError as err:
		print "Folder exist"
	os.chdir(iPath)
	plt.savefig('{}.{}'.format(name, fmt), fmt='png')
	os.chdir(pwd)
    #plt.close()
    
def createGraph(x, y, name, log):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.plot(x, y)
	plt.grid(True)
	if log:
		ax.set_xscale('log')
	save(name)
	plt.close(fig)
	return
	