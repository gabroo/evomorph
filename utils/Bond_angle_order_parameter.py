#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:38:00 2020

@author: georgecourcoubetis
"""

import sys
import csv
import glob,os
import numpy as np
import itertools as it
from matplotlib import pyplot as plt
import scipy as sp
from scipy import spatial


print("This script creates a perfect hexagonal lattice and demonstrates the ability of the bond angle order parmeters capability to score the pattern with a value of 1 for perfect down to 0 for completely disordered pattern")

print("\n")

print("variable length scale of hex lattice does not change order value but noise level decreases it see noise variable" )

print("\n")

def Perfect_lattice_pos(i,j,a,noise):
    i=i+1
    j=j+1
    return [a*i + a*(1/2)*(j%2)+np.random.random()*noise, a*j*(np.sqrt(3)/2)+np.random.random()*noise]

Size_x,Size_y = 10, 10
a=1
noise=0.*a

hex_lattice=[]
for i in range(0,Size_x):
    for j in range(0,Size_y):
        hex_lattice+=[Perfect_lattice_pos(i,j,a,noise)]
        

plt.scatter([r[0] for r in hex_lattice], [r[1] for r in hex_lattice] )

dela = sp.spatial.Delaunay
#triang = dela(lattice)

def find_neighbors(pindex, triang):
    neighbors = list()
    for simplex in triang.vertices:
        if pindex in simplex:
            neighbors.extend([simplex[i] for i in range(len(simplex)) if simplex[i] != pindex])
            '''
            this is a one liner for if a simplex contains the point we`re interested in,
            extend the neighbors list by appending all the *other* point indices in the simplex
            '''
    #now we just have to strip out all the dulicate indices and return the neighbors list:
    return list(set(neighbors))
def angl(a,b):
    ba = np.array(a) -np.array(b)
    c=complex(ba[0],ba[1])
    angle = np.angle(c)
    if angle<0:
        angle=2*np.pi+angle
    return angle

# 8/13/18 
def dist(a,b):
    ba = np.array(a) -np.array(b)
    return np.linalg.norm(ba)





def Bond_angle_order(lattice):
    nnAngl=[]
    order_contrib=[]
    triang = dela(lattice)
    for k in range(len(lattice)):
        nn=find_neighbors(k,triang)
        for i in range(len(nn)):
            angle=angl(lattice[nn[i]],lattice[k])
            nnAngl.append(angle)
            z=1j
            order_contrib+=[ np.exp(6*z*angle)/len(nn) ]
    tot=np.sum(order_contrib)
    tot=tot/len(lattice)
    tot= np.abs(tot)
    return tot, nnAngl

# boundary cells have non-consistent nearest neighbor angles contributing to the deviation from 
# an order parameter of 1

def Bond_angle_order_no_boundary(lattice):
    nnAngl=[]
    order_contrib=[]
    triang = dela(lattice)
    x=[r[0] for r in hex_lattice]
    y=[r[1] for r in hex_lattice]
    max_x=np.max(x)
    min_x=np.min(x)
    max_y=np.max(y)
    min_y=np.min(y)
    # number of boundary cells for modified normalization
    boundary_cells=0
    for k in range(len(lattice)):
        if lattice[k][0]==max_x or lattice[k][0]==min_x or lattice[k][1]==max_y or lattice[k][1]==min_y:
            boundary_cells+=1
            continue
        nn=find_neighbors(k,triang)
        for i in range(len(nn)):
            angle=angl(lattice[nn[i]],lattice[k])
            nnAngl.append(angle)
            z=1j
            order_contrib+=[ np.exp(6*z*angle)/len(nn) ]
    tot=np.sum(order_contrib)
    tot=tot/(len(lattice)-boundary_cells)
    tot= np.abs(tot)
    return tot, nnAngl


Order, angle_dist=Bond_angle_order(hex_lattice)

print("bond angle order with boundary cells")
print(Order)

Order, angle_dist=Bond_angle_order_no_boundary(hex_lattice)


print("bond angle order without boundary cells")
print(Order)

plt.show()

















