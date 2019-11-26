"""
Object oriented modelling allows inheritence of attributes and methods. This is what we want 
to make use of when building our simulation classes: we start with a generic simulation class
containing those atributes and methods that all other classes share.

To begin with, it is note worhy that we instantiate an object of any simulation class by 
"only" providing three attributes. 

name : a string object as a name for the model simulation object
mar_env : an instance of the market enviroment class
corr : a flag(bool) indicating weather the object is correlated or not.


this illustrates the role of market enviroment class : to provide in a single step all data
and objects required for simulation and valuation. The methods of the generic class are:

1) generate time grid: 
        this method generates the time grid of relevent dates used for the simulation
        this task is the same for every simulation class.

2) get_instrument_values:
        Every simulation class has to return the ndarray object with the simulated instrument values
        (e.g simulated values of the stock price, index values, volatility or interest rate)
"""

import numpy as np 
import pandas as pd 

class base_simulation(object):
    """
    Providing base methods for siualtion classes.

    Attributes
    ==========
    name : string (name of the object)
    mar_env : instance of market_enviroment (market enviroment data for simulation)
    corr : Boolean (True if correlated with other models)


    Methods
    =======
    genegrate_time_grid : returns the time grid for simulation
    get_instrument_values : returns the current instrument values
    """

    def __init__(self, name, mar_env, corr):
    	try:
    		self.name = name
    		self.pricing_date = mar_env.pricing_date
    		self.initial_value = mar_env.get_constant("initial_value")
    		self.volatility = mar_env.get_constant("volatility")
    		self.final_date = mar_env.get_constant("final_date")
    		self.currency = mar_env.get_constant("currency")
    		self.frequency = mar_env.get_constant("frequency")
    		self.paths = mar_env.get_constant("paths")
    		self.discount_curve = mar_env.get_curve("discount_curve")
    		try:
    			self.time_grid = mar_env.get_list("time_grid")
    		except:
    			self.time_grid = None

    		try:
    			self.special_dates = mar_env.get_list("special_dates")
    		except:
    			self.special_dates = []

    		self.instruments = None
    		self.correlated = corr
    		if corr is true:
    			self.cholesky_matrix = mar_env.get_list("cholesky_matrix")
    			self.rn_set = mar_env.get_list("rn_set")[self.name]
    			self.random_numbers = mar_env.get_list("random_numbers")
    	except:
    		raise("Error Parsing Market Enviroment")

    def generate_time_grid(self):
    	start = self.pricing_date
    	end = self.final_date
    	# pandas date_range function
    	# freq e.g "B" for business day, "W" for weekly, "M" for monthly
    	time_grid = pd.date_range(start=start, end=end, freq=self.frequency).to_pydatetime()
    	time_grid = list(time_grid)
    	# enhance time_grid by start, end, and special_date 

    	if start not in time_grid:
    		time_grid.insert(0, start)
    	if end not in time_grid:
    		time_grid.append(end)
    	if len(self.special_dates) > 0:
    		# add all special dates
    		time_grid.exten(self.special_dates)
    		# delete duplicates 
    		time_grid = list(set(time_grid))
    		# sort list 
    		time_grid.sort()

    	self.time_grid = np.array(time_grid)

    def get_instrument_values(self, fixed_seed=true):
        if instrument_values is None:
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.0)
        elif fixed_seed is False:
        	self.generate_paths(fixed_seed=fixed_seed, day_count=365.0)
        return self.instrument_values

