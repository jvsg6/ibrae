#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
from math import exp

import sqlite3
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.integrate import quad
import numpy as np

def save(name='', fmt='png'):
	pwd = os.getcwd()
	iPath = './pictures/{}'.format(fmt)
	try:
		os.makedirs(iPath)
	except:
		print "Folder exist"
	os.chdir(iPath)
	plt.savefig('{}.{}'.format(name, fmt), fmt='png')
	os.chdir(pwd)
    #plt.close()

rcParams['font.family'] = 'fantasy'
rcParams['font.fantasy'] = 'Arial'



def integrand(x, a, b):
	return a*x**2 + b
	
"""
dictNuclide = { "e_plane_srf_ad": 3.8e-16,
		"l"             : 1.0e-06,
		"e_air_sh_ad"   : 1.8e-14,
		"e_inh_ad"      : 7.4e-09,
		"e_ing_inf"     : 1.8e-07,
		}	
"""
def intWeat(t, dictNuclide):
	l = dictNuclide["l"]
	b1 = 3.59e-08
	b2 = 2.37e-10
	Wg = 0.63*exp(-b1*t)+0.37*exp(-b2*t)
	#print "Wg"
	#print Wg
	#print "t", t
	return Wg*exp(-l*t)
	
def intTgr_air(t, dictNuclide):
	l = dictNuclide["l"]
	T =  1e-05
	t0 = 86400
	if 0<=t<=t0:
		#print "aaaaaaaaaa"
		Tgr_air = T
	else:
		Tgr_air = T*t0/t+1e-09
	return Tgr_air*exp(-l*t)
	
def intTgr_gi(t, dictNuclide):
	l = dictNuclide["l"]
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
	
"""
def calcWI(dictNuclide, t):
	#I = quad(integrand, 0, 1, args=(a,b))
	l = dictNuclide["l"]
	I = quad(intWeat, 0, t, args = (dictNuclide))
	print "Wi"
	print I
	return I[0]
"""
def calcWI(dictNuclide, t):
	#I = quad(integrand, 0, 1, args=(a,b))
	l = dictNuclide["l"]
	b1 = 3.59e-08
	b2 = 2.37e-10
	#print "lambda", l, 1.5876780E-07
	I = 0.63*((1-exp(-(b1+l)*t))/(b1+l))+0.37*((1-exp(-(b2+l)*t))/(b2+l))
	#print "I tyt"
	#print "\nWi", I
	return I

def calcTI(dictNuclide, t):
	l = dictNuclide["l"]
	TI = quad(intTgr_air, 0, t, args = (dictNuclide))
	return TI[0]

def calcTI2(dictNuclide, t):
	l = dictNuclide["l"]
	TI = quad(intTgr_gi, 0, t, args = (dictNuclide))
	return TI[0]

def calc_e_gr_sh(dictNuclide, t):
	CorFgrd = 0.7
	SFe = 1.4
	WI = calcWI(dictNuclide, t)
	#print
	#print "WI", WI
	Fsf = 0.4
	Fof = 0.6
	#print "\ndictNuclide['e_plane_srf_ad']", dictNuclide["e_plane_srf_ad"]
	#print "\ndictNuclide['e_plane_srf_ad']", dictNuclide["e_plane_srf_ad"]

	e_gr_sh = dictNuclide["e_plane_srf_ad"]*CorFgrd*SFe*WI*(Fsf*Fof+(1-Fof))
	#print e_gr_sh
	return e_gr_sh
	
	
def calc_e_air_sh(dictNuclide, t):
	e_air_sh_ad = dictNuclide["e_air_sh_ad"]
	#TI = calcTI(dictNuclide, t)
	#print "TI", TI
	if t<604899:
		TI = 2.47061716777676
	else:
		TI = 4.08164341687635
	SFe = 1.4
	e_air_sh = e_air_sh_ad*TI*SFe
	return e_air_sh
	
def calc_e_inh_res(dictNuclide, t):
	#e_inh_ad = dictNuclide["e_inh_ad"]
	e_inh_ad = 7.9e-09
	#TI = calcTI(dictNuclide, t)
	if t<604899:
		TI = 2.47061716777676
	else:
		TI = 4.08164341687635
	#print "TI", TI
	Frf = 1
	Qair = 3.333333333333e-04
	e_inh_res = e_inh_ad*TI*Frf*Qair
	return e_inh_res

def calc_e_ind_ing(dictNuclide, t):
	#TI_inf = calcTI2(dictNuclide, t)
	TI_inf = 0
	if t<604899:
		TI_inf = 0.000178683905355862
	else:
		TI_inf = 0.000294811405355862
	#print "TI_inf", TI_inf
	#e_ing_in = dictNuclide["e_ing_inf"]
	e_ing_in = 1.8e-08
	e_ind_ing = e_ing_in*TI_inf
	return e_ind_ing

	
def calcEgrd(dictNuclide, t):
	Egr = calc_e_gr_sh(dictNuclide, t)+calc_e_air_sh(dictNuclide, t)+calc_e_inh_res(dictNuclide, t)+calc_e_ind_ing(dictNuclide, t)
	print "time", t
	print "1)calc_e_gr_sh(dictNuclide, t)", calc_e_gr_sh(dictNuclide, t)
	print "2)calc_e_air_sh(dictNuclide, t)", calc_e_air_sh(dictNuclide, t)
	print "3)calc_e_inh_res(dictNuclide, t)", calc_e_inh_res(dictNuclide, t)
	print "4)calc_e_ind_ing(dictNuclide, t)", calc_e_ind_ing(dictNuclide, t)
	return Egr


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
	dictNuclide = {}
	print "--------------------------------------------"
	#Устанавливаем соединение с базой данных
	conn = sqlite3.connect('./db/new_db.sqlite')
	
	# Создаем курсор - это специальный объект который делает запросы и получает их результаты
	cursor = conn.cursor()
		
	for i in range(1,6):
		cursor.execute("SELECT e_plane_srf_ad FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		dictNuclide.update({"e_plane_srf_ad" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT e_air_sh_ad FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		dictNuclide.update({"e_air_sh_ad" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT e_inh_ad FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		dictNuclide.update({"e_inh_ad" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT e_ing_inf FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		dictNuclide.update({"e_ing_inf" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT Decay_const FROM Table_6_Half_life_adn_decay_const WHERE id={0}".format(i))
		dictNuclide.update({"l" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT nuclide FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		nuclide = cursor.fetchall()[0][0]
		print 
		print nuclide
		print  
		print calcEgrd(dictNuclide, 604800)
		print
		print calcEgrd(dictNuclide, 31536000)
		print "--------------------------------------------"
	#Закрываем соединение с базой данных
	conn.close()
	#x = range(0,31536000, 6000)
	#y = [calcEgrd(time) for time in x]
	#createGraph(x, y, "FromDayToYearLog", True)
	#createGraph(x, y, "FromDayToYear", False)
	return
	
if __name__=="__main__":
	sys.exit(main())