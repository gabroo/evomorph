'''
Random calculations for some parameters.

TODO:
- vectorization
- magic numbers
'''
import math
import numpy as np
from scipy.spatial import Delaunay

def mitosis_force_min(alpha):
	'''
	Negative mitosis driving force fluctuation, based on an exponential parameter alpha.
	'''
	return -3*10**(alpha) # TODO what is this

def mitosis_force_max(alpha):
	'''
	Positive mitosis driving force fluctuation, based on an exponential parameter alpha.
	'''
	return 4*10**(alpha) # TODO what is this

def sphere_vol(r):
	'''
	Volume of a sphere
	'''
	return (4/3)*math.pi*(r**3)

def sphere_sa(r):
	'''
	Surface area of a sphere
	'''
	return 4*math.pi*(r**2)

# bond angle order stuff

def find_neighbors(pindex, triang):
    neighbors = list()
    for simplex in triang.vertices:
        if pindex in simplex:
            neighbors.extend([simplex[i] for i in range(len(simplex)) if simplex[i] != pindex])
    return list(set(neighbors))

def angl(a,b):
    ba = np.array(a) -np.array(b)
    c=complex(ba[0],ba[1])
    angle = np.angle(c)
    if angle<0:
        angle=2*np.pi+angle
    return angle

def dist(a,b):
    ba = np.array(a) -np.array(b)
    return np.linalg.norm(ba)

def bond_angle_order(lattice,nearest_neighbors=6):
    nnAngl=[]
    order_contrib=[]
    triang = Delaunay(lattice)
    x=[r[0] for r in lattice]
    y=[r[1] for r in lattice]
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
            order_contrib+=[ np.exp(nearest_neighbors*z*angle)/len(nn) ]
    tot=np.sum(order_contrib)
    tot=tot/(len(lattice)-boundary_cells)
    tot= np.abs(tot)
    return tot #, nnAngl