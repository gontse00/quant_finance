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

#===================================================================================
#create market environment for geometric brownian motion (GBM)
me_gbm = market_enviroment("me_gbm", dt.datetime(2015, 1, 1))
me_gbm.add_constant("initial_value", 36.)
me_gbm.add_constant("volatility", 0.2)
me_gbm.add_constant("currency", "ZAR")
me_gbm.add_constant("model", "gbm")

#create market environment for jump deffusion (JD)
me_jd = market_enviroment("me_jd", me_gbm.pricing_date)
me_jd.add_constant("lambda", 0.3)
me_jd.add_constant("mu", -0.75)
me_jd.add_constant("delta", 0.1)
me_jd.add_constant("model", "jd")
me_jd.add_enviroment(me_gbm)
#==================================================================================



#===================================================================================
#create market environment and positions environment for call option
me_eur_call = market_enviroment("me_call", me_jd.pricing_date)
me_eur_call.add_constant("strike", 38.0)
me_eur_call.add_constant("maturity", dt.datetime(2015, 12, 31))
me_eur_call.add_constant("currency", "ZAR")
call_payoff = 'np.maximum(maturity_value-strike, 0)'
european_call_positions = positions(
    name="european call",
    quantity=5,
    underlying="jd",
    mar_env=me_eur_call,
    otype="European",
    payoff_func=call_payoff)
european_call_positions.get_info()
#===================================================================================


#==================================================================================
#create market environment for european put
me_eur_put = market_enviroment("me_eur_put", dt.datetime(2015, 1, 1))
me_eur_put.add_constant("strike", 40.)
me_eur_put.add_constant("maturity", dt.datetime(2015, 12, 31))
me_eur_put.add_constant("currency", "ZAR")
put_payoff = 'np.maximum(strike-maturity_value,0)'
european_put_positions = positions(
    name="european put",
    quantity=2,
    underlying="gbm",
    mar_env=me_eur_put,
    otype="European",
    payoff_func=put_payoff)
european_put_positions.get_info()
#==================================================================================




#==================================================================================
#create a market environment and positions environment for american put
me_ame_put = market_enviroment("me_ame_put", dt.datetime(2015, 1, 1))
me_ame_put.add_constant("maturity", dt.datetime(2015, 12, 31))
me_ame_put.add_constant("strike", 40.)
me_ame_put.add_constant("currency", "ZAR")
ame_put_payoff = 'np.maximum(strike - instrument_values, 0)'
american_put_positions = positions(
    name="american put",
    quantity=3,
    underlying="gbm",
    mar_env=me_ame_put,
    otype="American",
    payoff_func=ame_put_payoff)
american_put_positions.get_info()
#======================================================================================



#====================================================================================
#create environment for portfolio valuation
csr = short_rate("csr", 0.06)
val_env = market_enviroment("general", me_jd.pricing_date)
val_env.add_constant("frequency", "W")
val_env.add_constant("paths", 25000)
val_env.add_constant("starting_date", val_env.pricing_date)
val_env.add_constant("final_date", val_env.pricing_date)
val_env.add_curve("discount_curve", csr)

positions = {
    "eur_call_pos": european_call_positions,
    "ame_put_pos": american_put_positions,
    "eur_put_pos": european_put_positions
}
underlyings = {"gbm": me_gbm, "jd": me_jd}

der_port = derivatives_portfolio(
    name="portfolio",
    positions=positions,
    val_env=val_env,
    assets=underlyings,
    fixed_seed=True
)
#american_put_positions.get_info()
#der_port.get_positions()
port_stats = der_port.get_statistics()
print(port_stats)
#american_positions.get_info()