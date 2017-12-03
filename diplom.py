#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os

from math import cos,sin,radians,sqrt,fabs,acos,pi,degrees,floor, exp
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def f1(y, t):
	a=2
	b=3
	c=4
	v=a*b*c
	s=2*(a*b+a*c+b*c)
	Fgs=10**(-2)*s/v
	y1, y2 = y
	return [-Fgs*y1+Fgs*y2,Fgs*y1-Fgs*y2]
	
def f2(y, t):
	a=2
	b=3
	c=4
	s=a*b+a*c+b*c+a*b+a*c+b*c #b*c - пол
	v=a*b*c
	T=300
	R=8.31
	BAS4=4*10**(-3)
	BAS62=5*10**(-9)
	BAS76=1*10**(-5)
	print s, v, float(s)/float(v)
	EAKT4=0
	EAKT62=8.22*10**4
	EAKT76=0
	
	k4=BAS4
	k62=BAS62*exp((EAKT62*(T-298.5))/(T*R*298.5))
	k76=BAS76
	k77=0
	
	
	
	y1, y2, y3 = y
	return [-k4*y1*s/v+k62*s/v*y2, k4*y1-k62*y2-k76*y2+k77*y3*0.5, k76*y2-k77*y3]

def main():
	fig = plt.figure(facecolor='white')
	y0 = [1.0, 0.0]
	t = np.linspace(0.0,4000.0,500.0) # вектор моментов времени
	[y1,y2]=odeint(f1, y0, t, full_output=False).T
	plt.plot(t,y1, linewidth=2) # график решения x(t) слева
	plt.plot(t,y2, linewidth=2) # фазовая траектория справа
	plt.grid(True)
	#y0 = [1.0, 0.0] # начальное значение
	#y = odeint(dydt, y0, t) # решение уравнения
	#y = np.array(y).flatten() # преобразование массива
	#plt.plot(t, y,'-sr',linewidth=3) # построение графика
	fig2=plt.figure(facecolor='white')
	t = np.linspace(0.0,40000.0,500.0)
	y0 = [1.0, 0.0, 0.0]
	[y1,y2, y3]=odeint(f2, y0, t, full_output=False).T
	plt.plot(t,y1, linewidth=2) # график решения x(t) слева
	plt.plot(t,y2, linewidth=2) # фазовая траектория справа
	plt.plot(t,y3, linewidth=2) # график решения x(t) слева
	plt.grid(True)
	plt.show()
	return

if __name__ == "__main__":
	sys.exit(main())
