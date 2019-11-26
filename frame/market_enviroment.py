### Market Enviroments
"""
Market enviroments is just a name for a collection of other data and python objects.
This abstraction simplifies a number of operations and also allows for a consistant modeling of recuring aspects.

A market enviroment consists of three dicts to store the following types of data and python objects.

1) constants: these can be model params or option maturity date.
2) Lists: These are sequences of objects in general, like a list object of objects modelling (risky) securities
3) Curves: These are objects for discounting, for example, like an instance of a short_rate class.
"""

"""
This is a storage class, for practical applications, market data and other data as well as Python 
Objects are first collected, then a market_enviroment object is instantiated and filled with the relevent 
data objects. this is then delivered in a sigle step to other classes that need the data and objects in 
the respective market_enviroment objects.

A major advantage of this object orientaed modeling aproach is, for example, that instances of the short_rate
class can live in multiple market enviroments. Once the instanceis updated, for example, when a new costant 
short rate is set, all the instances of the market_enviroment class containing that particular instance of the
discounting class will be updated automtically.
"""
class market_enviroment(object):
	"""
	class to model a market enviroment relevent for valuation.

	Attributes
	==========
	name : string (name of market enviroment)
	pricing_date : datetime object (date of market enviroment)

	Methods
	=======
	add_constant : adds constant (e.g model param)
	get_constant : gets a constant
	
	add_list : adds a list (e.g underlyngs, dates etc)
	get_list : gets a list

	add_curve : add a market curve (e.g yield curve)
	get_curve : get a market curve

	add_enviroment : ads and overwrites whole market enviroments with constatns, lists and curves.
	"""

	def __init__(self, name, pricing_date):
		self.name = name
		self.pricing_date = pricing_date
		self.constants = {}
		self.lists = {}
		self.curves = {}

	def add_constant(self, key, constant):
		self.constants[key] = constant
	def get_constant(self, key):
		return self.constant[key]

	def add_list(self, key, list_object):
		self.lists[key] = list_object
	def get_list(self, key):
		return self.lists[key]

	def add_curve(self, key, curve):
		self.curves[key] = curve
	def get_curve(self, key):
		return self.curves[key]

	def add_enviroment(self, env):
		for key in env.constants:
			self.constants[key] = env.constants[key]

		for key in env.lists:
			self.lists[key] = env.lists[key]

		for key in env.curves:
			self.curves[key] = env.curves[key]



