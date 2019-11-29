import numpy as np
from random_number_generator.standard_normal_rn import standard_normal_rn
from .base_simulation import base_simulation


class geometric_brownian_motion(base_simulation):
    """
	Class to gengerate simulated paths based on the Black Scholes model.

	Attributes
	==========
	name : string (name of object)
	mar_env : instance of market_enviroment
	corr : boolean

	Methods
	=======
	update : updates parameters
	generate_paths : returns monte_carlo paths given the market enviroment
	"""

    def __init__(self, name, mar_env, corr=False):
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=False, day_count=365.0):
        if self.time_grid is None:
            self.generate_time_grid()
        # number of dates for time grid
        M = len(self.time_grid)
        # number of paths
        I = self.paths
        paths = np.zeros((M, I))
        paths[0] = self.initial_value

        if not self.correlated:
            rand = standard_normal_rn((1, M, I))
        else:
            rand = self.random_numbers

        short_rate = self.discount_curve.short_rate

        for t in range(1, len(self.time_grid)):
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            paths[t] = paths[t - 1] * np.exp(
                (short_rate - 0.5 * self.volatility ** 2) * dt + self.volatility * np.sqrt(dt) * ran)

        self.instrument_values = paths
