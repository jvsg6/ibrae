#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
from math import exp


import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.integrate import quad
import numpy as np

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

rcParams['font.family'] = 'fantasy'
rcParams['font.fantasy'] = 'Arial'


	
	
dictNucl = {    "e_pl_srf": 3.8e-16,
		"l"       : 1.0e-06,
		"e_air_sh_ad" : 1.8e-14,
		"e_inh_ad" : 7.4e-09,
		"e_ing_in" : 1.8e-07,
		"eing_inf" : 1.8e-07,
		"eing_ad"  : 2.2e-08,
		"delta_eff": 6.4e+05,
		"Fcons"    : 9.2e-01,
		}	



def calc_e_ing_pre(t):
	f1 = 3
	Fmilk = 0.5
	Ucow = 1.9e-04
	Fcow_feed = 0.7
	Tfeed_cow_milk = 4.7e+02
	
	Qmilk_inf = 3.8e-06
	eing_inf = dictNucl["eing_inf"]
	Qmilk_ad = 3.3e-06
	eing_ad = dictNucl["eing_ad"]
	max_milk = max(Qmilk_inf*eing_inf, Qmilk_ad*eing_ad)
	
	Qlv_inf = 6.3e-07
	eing_inf = dictNucl["eing_inf"]
	Qlv_ad = 1.9e-06
	eing_ad = dictNucl["eing_ad"]
	max_lv = max(Qlv_inf*eing_inf, Qlv_ad*eing_ad)
	
	f2 = 0.3
	Flv = 0.5
	delta_eff = dictNucl["delta_eff"]
	Fcons = dictNucl["Fcons"]
	e_ing_pre = (f1*Fmilk*Ucow*Fcow_feed*Tfeed_cow_milk*max_milk+max_lv*f2*Flv)*delta_eff*Fcons
	#print "time", t
	return e_ing_pre

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
	

def main():
	print 
	print calc_e_ing_pre(604800)
	print
	print calc_e_ing_pre(31536000)
	#x = range(0,31536000, 6000)
	#y = [calcEgrd(time) for time in x]
	#createGraph(x, y, "FromDayToYearLog", True)
	#createGraph(x, y, "FromDayToYear", False)
	return
	
if __name__=="__main__":
	sys.exit(main())