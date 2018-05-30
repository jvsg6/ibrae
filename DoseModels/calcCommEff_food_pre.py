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
	except WindowsError as err:
		print "Folder exist"
	os.chdir(iPath)
	plt.savefig('{}.{}'.format(name, fmt), fmt='png')
	os.chdir(pwd)
    #plt.close()

rcParams['font.family'] = 'fantasy'
rcParams['font.fantasy'] = 'Arial'


def calc_e_ing_pre(dictNucl):
	f1 = 3.0 #
	Fmilk = 0.5 #
	Ucow = 1.851852E-04 #
	Fcow_feed = 0.7 #
	Tfeed_cow_milk = dictNucl["T_feed_cow_milk"] 
	
	Qmilk_inf = 3.805175E-06 #
	eing_inf = dictNucl["e_ing_inf"] 
	Qmilk_ad = 3.329528E-06 #
	eing_ad = dictNucl["e_ing_ad"] 
	max_milk = max(Qmilk_inf*eing_inf, Qmilk_ad*eing_ad)
	
	Qlv_inf = 6.341958E-07 #
	eing_inf = dictNucl["e_ing_inf"] 
	Qlv_ad = 1.902588E-06 #
	eing_ad = dictNucl["e_ing_ad"] 
	max_lv = max(Qlv_inf*eing_inf, Qlv_ad*eing_ad)
	
	f2 = 0.3 
	Flv = 0.5
	delta_eff = dictNucl["del_eff_OLI_3"] #
	Fcons = dictNucl["F_cons"] #
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

	dictNuclide = {}
	print "--------------------------------------------"
	#Устанавливаем соединение с базой данных
	conn = sqlite3.connect('./db/new_db.sqlite')
	
	# Создаем курсор - это специальный объект который делает запросы и получает их результаты
	cursor = conn.cursor()
		
	for i in range(1,6):
		cursor.execute("SELECT T_feed_cow_milk FROM Table_21_Transfer_factor_from_feed_to_milk WHERE id={0}".format(i))
		dictNuclide.update({"T_feed_cow_milk" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT e_ing_inf FROM Table_27_Dose_conv_for_Food_pre_and_post_analysis WHERE id={0}".format(i))
		dictNuclide.update({"e_ing_inf" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT e_ing_ad FROM Table_27_Dose_conv_for_Food_pre_and_post_analysis WHERE id={0}".format(i))
		dictNuclide.update({"e_ing_ad" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT del_eff_OLI_3 FROM Table_20_Effective_availability_period WHERE id={0}".format(i))
		dictNuclide.update({"del_eff_OLI_3" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT F_cons FROM Table_22_Fraction_remaining_human_consumption WHERE id={0}".format(i))
		dictNuclide.update({"F_cons" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT Decay_const FROM Table_6_Half_life_adn_decay_const WHERE id={0}".format(i))
		dictNuclide.update({"l" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT nuclide FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		nuclide = cursor.fetchall()[0][0]
		print 
		print nuclide
		print  
		print calc_e_ing_pre(dictNuclide)
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