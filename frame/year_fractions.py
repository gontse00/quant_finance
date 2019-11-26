### MOdelling and handling dates
"""
A necessary pre-requisite for discounting the modeling of dates. For valuation purposes one typically divides 
the time interval between today and the final date of the general market model T into descrete time intervals.
The time intervals can be homogeneous(i.e. of equal length), or they be of heterogeneous (of varying length).
A valuation library should be able to handle the more general case of heterogeneous time intervals.

We work with a *list* of *dates* assuming the smallest relevent time interval is 1 day. We do not care about intraday events. Theres 2 aproaches to compile a list of dates, 
i) Constructing a list of conrete dates(e.g datetime.datetime objects)
ii)year fractions (as decimals, as is often done in theory)
"""


import numpy as np 

def year_fractions(date_list, day_count=365.):
	"""
	return a vector of floats with day fractions in years.
	Initial value normalized to zero.

	Params
	======

	i) date_list: list (collection of datetime objects)
	ii) day_count float (to account for differnt conventions)

	Returns
	=======
	i) delta_list: array (year fractions)
	"""

	start = date_list[0]
	delta_list = [(date-start).days/day_count for date in date_list]
	return np.array(delta_list)
	
