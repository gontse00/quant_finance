class base_valuation(object):
    """
    Base class for single factor valuation

	Attributes
	==========
	name : string (name of the object)
	underlying : instance of simulation classs
	mar_env : instance of market enviroment 
	payoff_func : 
	    string (derivatives payoff in python syntax e.g 'np.maximum(maturity_value-K,0)'
	    where maturity_value is anumpy vector with respective vaues of the underlying.

	    example 'np.maximum(instrument_values-K,0)' where instrument_values are a numpy 
	    matrix with values of the underlying over the whole time/path grid.

	Methods
	=======
	update : updates selected valuation params
	delta : returns the elta of the derivative
	vega : returns the Vega of the derivative.
	"""

    def __init__(self, name, underlying, mar_env, payoff_func=''):
        try:
            self.name = name
            self.pricing_date = mar_env.pricing_date
            try:
                self.strike = mar_env.get_constant("strike")
            except:
                pass
            self.maturity = mar_env.get_constant("maturity")
            self.currency = mar_env.get_constant("currency")
            self.frequency = underlying.frequency
            self.paths = underlying.paths
            self.discount_curve = underlying.discount_curve
            self.payoff_func = payoff_func
            self.underlying = underlying
            try:
                self.underlying.special_dates.extend([self.pricing_date, self.maturity])
            except:
                print("cannot extend special dates")

        except:
            print("error parsing valuation market enviroment")

    def update(self, initial_value=None, volatility=None, strike=None, maturity=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if strike is not None:
            self.strike = strike
        if maturity is not None:
            self.maturity = maturity
            if not maturity in self.underlying.time_gridd:
                self.underlying.special_dates.append(maturity)
                self.underlying.instrument_values = None

    def delta(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value / 50.0
        value_left = self.present_value(fixed_seed=True)
        initial_del = self.underlying.initial_value + interval
        self.underlying.update(initial_value=initial_del)
        value_right = self.present_value(fixed_seed=True)
        self.underlying.update(initial_value=initial_del - interval)
        delta = (value_right - value_left) / interval

        if delta < -1.0:
            return -1.0
        elif delta > 1.0:
            return 1.0
        else:
            return round(delta, accuracy)

    def vega(self, interval=0.01, accuracy=4):
        if interval < self.underlying.volatility / 50.0:
            interval = self.underlying.volatility / 50.0
        value_left = self.present_value(fixed_seed=True)
        vola_del = self.underlying.volatility + interval
        self.underlying.update(volatility=vola_del)
        value_right = self.present_value(fixed_seed=True)
        self.underlying.update(volatility=vola_del - interval)
        vega = (value_right - value_left) / interval
        return round(vega, accuracy)
