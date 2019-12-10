import numpy as np
import pandas as pd
from random_number_generator.standard_normal_rn import standard_normal_rn
from valuation.european_valuation import european_valuation
from valuation.american_valuation import american_valuation
from simulation.geometric_brownian_motion import geometric_brownian_motion
from simulation.jump_deffusion import jump_deffusion
from simulation.square_root_deffusion import square_root_deffusion


models = {
    'gbm': geometric_brownian_motion,
    'jd': jump_deffusion,
    'srd': square_root_deffusion
}

otypes = {
    'European': european_valuation,
    'American': american_valuation
}

class derivatives_portfolio(object):
    """
    class for building a portfolio of derivatives positions
    """

    def __init__(self, name, positions, val_env, assets, correlations=None, fixed_seed=False):
        self.name = name
        self.positions = positions
        self.val_env = val_env
        self.assets = assets
        self.underlyings = set()
        self.correlations = correlations
        self.time_grid = None
        self.underlying_objects = {}
        self.valuation_objects = {}
        self.fixed_seed = fixed_seed
        self.special_dates = []

        for pos in self.positions:
            self.val_env.constants['starting_date'] = min(self.val_env.constants['starting_date'],
                                                          positions[pos].mar_env.pricing_date)
            self.val_env.constants['final_date'] = max(self.val_env.constants['final_date'],
                                                       positions[pos].mar_env.pricing_date)
            self.underlyings.add(positions[pos].underlying)

        start = self.val_env.constants['starting_date']
        end = self.val_env.constants['final_date']
        time_grid = pd.date_range(start=start, end=end, freq=self.val_env.constants['frequency']).to_pydatetime()
        time_grid = list(time_grid)

        for pos in self.positions:
            maturity_date = positions[pos].mar_env.constants['maturity']
            if maturity_date not in time_grid:
                time_grid.insert(0, maturity_date)
                self.special_dates.append(maturity_date)

        if start not in time_grid:
            time_grid.insert(0, start)

        if end not in time_grid:
            time_grid.append(end)

        time_grid = list(set(time_grid))
        time_grid.sort()
        self.time_grid = np.array(time_grid)
        self.val_env.add_list('time_grid', self.time_grid)

        if correlations is not None:
            ul_list = sorted(self.underlyings)
            correlation_matrix = np.zeros((len(ul_list), len(ul_list)))
            np.fill_diagonal(correlation_matrix, 1.0)
            correlation_matrix = pd.DataFrame(correlation_matrix, index=ul_list, columns=ul_list)

            for i, j, corr in correlations:
                corr = min(corr, 0.999999999999)
                correlation_matrix.loc[i, j] = corr
                correlation_matrix.loc[j, i] = corr
            cholesky_matrix = np.linalg.cholesky(np.array(correlation_matrix))

            rn_set = {
                asset: ul_list.index((asset)) for asset in self.underlyings
            }

            random_numbers = standard_normal_rn(
                (len(rn_set), len(self.time_grid), self.val_env.constants["paths"]),
                fixed_seed=self.fixed_seed
            )

            self.val_env.add_list("cholesky_matrix", cholesky_matrix)
            self.val_env.add_list("random_numbers", random_numbers)
            self.val_env.add_list("rn_set", rn_set)

        for asset in self.underlyings:
            mar_env = self.assets[asset]
            mar_env.add_enviroment(val_env)
            model = models[mar_env.constants['model']]

            if correlations is not None:
                self.underlying_objects[asset] = model(asset, mar_env, corr=True)
            else:
                self.underlying_objects[asset] = model(asset, mar_env, corr=False)

        for pos in positions:
            val_class = otypes[positions[pos].otype]
            mar_env = positions[pos].mar_env
            mar_env.add_enviroment(self.val_env)
            self.valuation_objects[pos] = \
            val_class(name=positions[pos].name,
                      mar_env=mar_env,
                      underlying=self.underlying_objects[positions[pos].underlying],
                      payoff_func=positions[pos].payoff_func)

    def get_positions(self):
        for pos in self.positions:
            bar = '\n' + 50*'-'
            print(bar)
            self.positions[pos].get_info()
            print(bar)

    def get_statistics(self, fixed_seed=False):
        res_list = []
        for pos, value in self.valuation_objects.items():
            p = self.positions[pos]
            pv = value.present_value(fixed_seed=fixed_seed)
            res_list.append([
                p.name,
                p.quantity,
                pv,
                value.currency,
                pv*p.quantity,
                value.delta()*p.quantity,
                value.vega()*p.quantity,
            ])
        res_df = pd.DataFrame(res_list,
                              columns=['name', 'qty', 'value', 'curr', 'pos_value', 'pos_delta', 'pos_vega'])
        return res_df
