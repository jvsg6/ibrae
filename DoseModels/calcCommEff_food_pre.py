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



def integrand(x, a, b):
	return a*x**2 + b
	
	
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

def intWeat(t):
	l = dictNucl["l"]
	b1 = 3.59e-08
	b2 = 2.37e-10
	Wg = 0.63*exp(-b1*t)+0.37*exp(-b2*t)
	return Wg*exp(-l*t)
	
def intTgr_air(t):
	l = dictNucl["l"]
	T =  1e-05
	t0 = 86400
	if 0<=t<=t0:
		#print "aaaaaaaaaa"
		Tgr_air = T
	else:
		Tgr_air = T*t0/t+1e-09
	return Tgr_air*exp(-l*t)
	
def intTgr_gi(t):
	l = dictNucl["l"]
	Qsoil = 1.2e-09
	pdep = 1600.0
	d_ind = 0.001
	Fsolid = 1
	T = Qsoil/(pdep*d_ind*Fsolid)
	t0 = 86400
	#print "T for infant", T
	if 0<=t<=t0:
		#print "aaaaaaaaaa"
		Tgr_air = T
	else:
		Tgr_air = T*t0/t
	return Tgr_air*exp(-l*t)
	

#def calcWI(t):
#	#I = quad(integrand, 0, 1, args=(a,b))
#	x = range(0, 8640001, 600)
#	I7d = quad(intWeat, 0, 604800, args = (l))
#	I1y = quad(intWeat, 0, 31536000, args = (l))
#	WI = {"7d":I7d[0], "1a":I1y[0]}
#	b1 = 3.59e-08
#	b2 = 2.37e-10
#	x = range(0, 30240000, 600)
#	Wg = [0.63*exp(-b1*t)+0.37*exp(-b2*t) for t in x]
#	createGraph(x, Wg, 'Wg', False)
#	return WI

def calcWI(t):
	#I = quad(integrand, 0, 1, args=(a,b))
	l = dictNucl["l"]
	I = quad(intWeat, 0, t)
	return I[0]

def calcTI(t):
	l = dictNucl["l"]
	TI = quad(intTgr_air, 0, t)
	return TI[0]

def calcTI2(t):
	l = dictNucl["l"]
	TI = quad(intTgr_gi, 0, t)
	return TI[0]

#def calcTI(l):
#	TI = quad(intRes, 0, 604800, args = (l))
#	print TI
#	x = range(0, 8640001, 600)
#	TI = [quad(intRes, 0, time, args = (l))[0] for time in x]
#	createGraph(x, TI, 'TI', True)
#	
#
#	x = range(0, 8640001, 600)
#	y = [calcT(time) for time in x]
#	createGraph(x, y, 'T', True)
#	return TI


def calc_e_gr_sh(t):
	CorFgrd = 0.7
	SFe = 1.4
	WI = calcWI(t)
	#print "WI", WI
	Fsf = 0.4
	Fof = 0.6
	e_gr_sh = dictNucl["e_pl_srf"]*CorFgrd*SFe*WI*(Fsf*Fof+(1-Fof))
	return e_gr_sh
	
	
def calc_e_air_sh(t):
	e_air_sh_ad = dictNucl["e_air_sh_ad"]
	TI = calcTI(t)
	#print "TI", TI
	SFe = 1.4
	e_air_sh = e_air_sh_ad*TI*SFe
	return e_air_sh
	
def calc_e_inh_res(t):
	e_inh_ad = dictNucl["e_inh_ad"]
	TI = calcTI(t)
	#print "TI", TI
	Frf = 1
	Qair = 3.3e-04
	e_inh_res = e_inh_ad*TI*Frf*Qair
	return e_inh_res

def calc_e_ind_ing(t):
	TI_inf = calcTI2(t)
	#print "TI_inf", TI_inf
	e_ing_in = dictNucl["e_ing_in"]
	e_ind_ing = e_ing_in*TI_inf
	return e_ind_ing



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
	e_ing_pre = f1*Fmilk*Ucow*Fcow_feed*Tfeed_cow_milk*max_milk*max_lv*f2*Flv*delta_eff*Fcons
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