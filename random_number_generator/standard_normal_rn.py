"""
Random number generation is a central task of Monte Carlo simulation.
For this projects at hand, standar normally distributed random numbers are the most import ones.
"""
import numpy as np 

def standard_normal_rn(shape, antithetic=False, moment_matching=True, fixed_seed=False):
	"""
	Functions to generate standard normal random numbers

	Params
	======
	shape : tuple(o,n,m) -> generate an array of shape (o,n,m)
	antithetic : boolean -> generation of antithetic variates 
	moment_matching : boolean -> matching of first and second moments
	fixed_seed : boolean -> flag to fix seed

	Returns
	=======
	ran : (o,n,m) -> array of random numbers
	"""

	if fixed_seed:
		np.random.seed(1000)
	
	if antithetic:
		ran = np.random.standard_normal((shape[0], shape[1], int(shape[2]/2)))
		ran = np.concatenate((ran, -ran), axis=2)
	else:
		ran = np.random.standard_normal(shape)

	if moment_matching:
		ran = ran - np.mean(ran)
		ran = ran/np.std(ran)

	if shape[0]==1:
		return ran[0]
	else:
		return ran
