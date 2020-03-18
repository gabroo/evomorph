'''
Random calculations for some parameters.

TODO:
- vectorization
- magic numbers
'''
import math

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