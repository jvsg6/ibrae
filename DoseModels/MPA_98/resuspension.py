#!/usr/bin/python2.7
# -*- coding: utf-8 -
import sys
import os
from os import path
from math import exp
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from AdditionalFunctions.createGraph import createGraph
import sqlite3


def calcK(t, l):
	K1 = 1e-5
	K2 = 1e-9
	l1 = 1.46e-7
	l2 = 2.2e-10
	return K1*exp(-(l1+l2+l)*t)+K2*exp(-(l2-l)*t)

def main():
	try:
		mypath = os.path.dirname(os.path.abspath(__file__))
	except NameError:
		mypath = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.chdir(mypath)
	x = [i for i in range(0, 31536001, 86400)]
	dictNuclide = {}
	print "--------------------------------------------"
	#Устанавливаем соединение с базой данных
	conn = sqlite3.connect('../db/new_db.sqlite')
	
	# Создаем курсор - это специальный объект который делает запросы и получает их результаты
	cursor = conn.cursor()
		
	for i in range(1,6):
		y = []
		cursor.execute("SELECT Decay_const FROM Table_6_Half_life_adn_decay_const WHERE id={0}".format(i))
		dictNuclide.update({"l" : cursor.fetchall()[0][0]})
		cursor.execute("SELECT nuclide FROM Table_24_Conversion_fraction_total_eff_dose_ground_scenario WHERE id={0}".format(i))
		nuclide = cursor.fetchall()[0][0]
		print 
		print nuclide
		print  
		for t in x:
			y.append(calcK(t, dictNuclide["l"]))
		createGraph(x, y, "{0}.png".format(nuclide), False, mypath)
		print "--------------------------------------------"
	#Закрываем соединение с базой данных
	conn.close()


	
	print "Done!!!"
	return

if __name__=="__main__":
	sys.exit(main())