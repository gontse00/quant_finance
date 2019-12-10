"""import datetime as dt 
from short_rate import short_rate
from market_enviroments import market_enviroment"""
import datetime as dt 
from frame import short_rate, market_enviroment, year_fractions
from random_number_generator.standard_normal_rn import standard_normal_rn 
from simulation.geometric_brownian_motion import *
from simulation.jump_deffusion import *
from simulation.square_root_deffusion import *
from valuation.european_valuation import european_valuation
from valuation.american_valuation import american_valuation
from portfolio.positions import positions
from portfolio.derivatives_portfolio import derivatives_portfolio

"""dates = [dt.datetime(2017, 1, 1), dt.datetime(2017, 2, 1), dt.datetime(2017, 3, 1),
dt.datetime(2017, 4, 1), dt.datetime(2017, 5, 1), dt.datetime(2017, 6, 1), dt.datetime(2017, 7, 1),
dt.datetime(2017, 8, 1), dt.datetime(2017, 9, 1), dt.datetime(2017, 10, 1),
dt.datetime(2017, 11, 1), dt.datetime(2017, 12, 1), dt.datetime(2018, 1, 1)]

deltas = year_fractions(dates)
csr = short_rate('csr', 0.06)
discount_factors = csr.get_discount_factors(dates)
#print(discount_factors)

mar_env = market_enviroment("test_env", dates[0])
mar_env.add_constant("drift", 0.1)
mar_env.add_constant("vol", 0.2)
mar_env.add_constant("diffusion", 0.3)
mar_env.add_curve('short_rate', csr)
mar_env.add_list("dates",discount_factors)

snrn = standard_normal_rn((1, 5, len(dates)))
#print(snrn)
"""

#create market enviroment for geometric brownian motion (GBM)
me_gbm = market_enviroment("me_gbm", dt.datetime(2015, 1, 1))
me_gbm.add_constant("initial_value", 36.)
me_gbm.add_constant("volatility", 0.2)
me_gbm.add_constant("final_date", dt.datetime(2015, 12, 31))
me_gbm.add_constant("frequency", "M")
me_gbm.add_constant("currency", "ZAR")
me_gbm.add_constant("model","gbm")
me_gbm.add_constant("paths", 10000)
csr = short_rate("csr", 0.06)
me_gbm.add_curve("discount_curve", csr)

#create market enviroment for jump deffusion (JD)
me_jd = market_enviroment("me_jd", me_gbm.pricing_date)
me_jd.add_constant("lambda", 0.3)
me_jd.add_constant("mu", -0.75)
me_jd.add_constant("delta", 0.1)
me_jd.add_constant("model", "jd")
me_jd.add_enviroment(me_gbm)

gbm = geometric_brownian_motion("gbm", me_gbm)
gbm.generate_time_grid()
jd = jump_deffusion("jd", me_jd)
jd.generate_time_grid()

#create market enviroment for call option
me_eur_call = market_enviroment("me_call", dt.datetime(2015, 1, 1))
me_eur_call.add_constant("strike", 40.)
me_eur_call.add_constant("maturity", dt.datetime(2015, 12, 31))
me_eur_call.add_constant("currency", "ZAR")
me_eur_call.add_constant("frequency", "M")
call_payoff = 'np.maximum(maturity_value-strike, 0)'
eur_call = european_valuation("call", underlying=gbm, mar_env=me_eur_call, payoff_func=call_payoff)
print(eur_call.present_value(), eur_call.delta(), eur_call.vega())

#create market enviroment for european put
me_eur_put = market_enviroment("me_eur_put", dt.datetime(2015, 1, 1))
me_eur_put.add_constant("strike", 40.)
me_eur_put.add_constant("maturity", dt.datetime(2015, 12, 31))
me_eur_put.add_constant("currency", "ZAR")
me_eur_put.add_constant("frequency", "M")
put_payoff = 'np.maximum(strike-maturity_value,0)'
eur_put = european_valuation("eur_put", underlying=jd, mar_env=me_eur_put, payoff_func=put_payoff)
print(eur_put.present_value(), eur_put.delta(), eur_put.vega())


#create positions enviroment
european_call_positions = positions(
    name="european call",
    quantity=20,
    underlying="jd",
    mar_env=me_eur_call,
    otype="European",
    payoff_func=call_payoff)

european_put_positions = positions(
    name="european put",
    quantity=35,
    underlying="gbm",
    mar_env=me_eur_put,
    otype="European",
    payoff_func=put_payoff)
#european_call_positions.get_info()
#european_put_positions.get_info()

#create enviroment for portfolio valuation
val_env = market_enviroment("general", me_jd.pricing_date)
val_env.add_constant("frequency", "M")
val_env.add_constant("paths", 25000)
val_env.add_constant("starting_date", val_env.pricing_date)
val_env.add_constant("final_date", val_env.pricing_date)
val_env.add_curve("discount_curve", csr)
underlyings = {"gbm": me_gbm, "jd": me_jd}
positions = {"call_positions":european_call_positions, "put_postions":european_put_positions}

der_port = derivatives_portfolio(
    name="portfolio",
    positions=positions,
    val_env=val_env,
    assets=underlyings,
    fixed_seed=True
)
der_port.get_positions()
port_stats = der_port.get_statistics()
print(port_stats)
#american_positions.get_info()
"""
me_jump = market_enviroment("jump_env", dt.datetime(2019,11,26))
me_jump.add_enviroment(me_gbm)
me_jump.add_constant("lambda", 0.8)
me_jump.add_constant("mu", -0.25)
me_jump.add_constant("delta", 0.1)

jd = jump_deffusion("jd",me_jump)
jd.generate_time_grid()
paths2 = jd.get_instrument_values()

me_srd = market_enviroment("me_srd", dt.datetime(2019,11,27))
me_srd.add_constant("initial_value", 0.25)
me_srd.add_constant("volatility", 0.035)
me_srd.add_constant("final_date", dt.datetime(2020,11,27))
me_srd.add_constant("currency", "EUR")
me_srd.add_constant("frequency", "B")
me_srd.add_constant("paths", 10000)

me_srd.add_constant("kappa", 4.0)
me_srd.add_constant("theta", 0.2)
me_srd.add_curve("discount_curve", 0.0)
srd = square_root_deffusion("srd", me_srd)
srd.generate_time_grid()
paths3 = srd.get_instrument_values()
"""