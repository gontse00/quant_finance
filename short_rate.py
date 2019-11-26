### We focus on the simplest case for discounting by the constant short rate. 
"""
Many option pricing models like the Black-Scholes(1973), Merton(1976), and Cor-Ross-Rubinstein(1979), make this assumption. Weassume continuous discounting, as is ussual for option pricing applications. 

the discount factors can also be interpreted as the value of a unit zero-coupon bond (ZCB) as of today.
""" 
from year_fractions import year_fractions
import numpy as np 

class short_rate(object):
	"""
	Class for shor rate discounting
	
	Attribute
	=========
	name: string(name of the object)
	short_rate: float (positive number)

	Methods
	=======
	get_discount_factors: get discount factors given a list/array of datetime objects or year fraction.
	"""

	def __init__(self, name, short_rate):
		self.name = name
		self.short_rate = short_rate
		if self.short_rate < 0:
			raise ValueError("short rate is negative")

	def get_discount_factors(self, date_list, dtobjects=True):
		if dtobjects is True:
			dlist = year_fractions(date_list)
		else:
			dlist = np.array(date_list)
		dflist = np.exp(self.short_rate*np.sort(-dlist))
		return np.array((date_list, dflist)).T 


