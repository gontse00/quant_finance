import numpy as np 
from random_number_generator.standard_normal_rn import standard_normal_rn
from .base_simulation import base_simulation 


class square_root_deffusion(base_simulation):
	"""
	Class to gengerate paths based on CIR (1985) square root deffusion model.

	Attribute
	=========
	name : string (name of object)
	mar_env : instance of market enviroment
	corr : boolean (true if correlated with other model object)

	Methods
	=======
	update : updates params
	generate_paths : return monte carlo paths given market enviroment
	"""

	def __init__(self, name, mar_env, corr=False):
		super(square_root_deffusion, self).__init__(name, mar_env, corr)
		try:
			self.kappa = mar_env.get_constant("kappa")
			self.theta = mar_env.get_constant("theta")
		except:
			print("Error Parsing market enviroment")

	def update(self, initial_value=None, volatility=None, kappa=None, theta=None, final_date=None):
		if initial_value is not None:
			self.initial_value = initial_value
		if volatility is not None:
			self.volatility = volatility
		if kappa is not None:
			self.kappa= kappa
		if theta is not None:
			self.theta = theta
		if final_date is not None:
			self.final_date = final_date
		self.instrument_values = None

	def generate_paths(self, fixed_seed=True, day_count=365.):
		if self.time_grid is None:
			self.generate_time_grid()
		M = len(self.time_grid)
		I = self.paths
		paths = np.zeros((M,I))
		paths_ =  np.zeros_like(paths)
		paths[0] = self.initial_value
		paths_[0] = self.initial_value

		if self.correlated is False:
			rand = standard_normal_rn((1,M,I), fixed_seed=fixed_seed)
		else:
			rand = self.random_numbers

		for t in range(1,len(self.time_grid)):
			dt = (self.time_grid[t]-self.time_grid[t-1]).days/day_count
			if self.correlated is False:
				ran = rand[t]
			else:
				ran = np.dot(self.cholesky_matrix, rand[:,t,:])
				ran = ran[self.rn_set]
			paths_[t]=(paths_[t-1]
				+self.kappa*(self.theta-np.maximum(0,paths_[t-1,:]))*dt
				+np.sqrt(np.maximum(0, paths_[t-1,:]))
				*self.volatility*np.sqrt(dt)*ran)
			paths[t] = np.maximum(0, paths_[t])
		self.instrument_values=paths