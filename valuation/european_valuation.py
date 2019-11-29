import numpy as np
from .base_valuation import base_valuation


class european_valuation(base_valuation):
    """
	class to value european options with arbitrary payoff by single facto
	monte carlo simulation.

	Methods
	=======
	generate_payoff : returns payoffs given the paths and the payoff fuction
	present_value : returns the present value (Monte carlo estimator)
	"""

    def generate_payoff(self, fixed_seed=False):
        """
		"""
        try:
            strike = self.strike
        except:
            pass
        paths = self.underlying.get_instrument_values(fixed_seed=fixed_seed)
        time_grid = self.underlying.time_grid
        try:
            time_index = np.where(time_grid == self.maturity)[0]
            time_index = int(time_index)
        except:
            print("Maturity date not in time index")
        maturity_value = paths[time_index]
        mean_value = np.mean(paths[:time_index], axis=1)
        max_value = np.amax(paths[:time_index], axis=1)[-1]
        max_value = np.amin(paths[:time_index], axis=1)[-1]
        try:
            payoff = eval(self.payoff_func)
            return payoff
        except:
            print("Error evaluation payoff")

    def present_value(self, accuracy=6, fixed_seed=False, full=False):
        """
		"""
        cash_flow = self.generate_payoff(fixed_seed=fixed_seed)
        discount_factor = self.discount_curve.get_discount_factors((self.pricing_date, self.maturity))[0, 1]
        result = discount_factor * np.sum(cash_flow) / len(cash_flow)

        if full:
            return round(result, accuracy), discount_factor * cash_flow
        else:
            return round(result, accuracy)
