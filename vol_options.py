import pandas as pd 
import numpy as np
import scipy.optimize as spo
from datetime import datetime as dt 
import calendar
from frame.market_enviroment import market_enviroment
from frame.short_rate import short_rate
from simulation.square_root_deffusion import square_root_deffusion
from valuation.european_valuation import european_valuation

vstoxx_index = pd.read_hdf("./data/vstoxx_march_2014.h5", key="vstoxx_index")
vstoxx_futures = pd.read_hdf("./data/vstoxx_march_2014.h5", key="vstoxx_futures")


"""def third_friday(date):
	day = 21-(calendar.weekday(date.year, date.month,1)+2)%7
	return dt(date.year, date.month, day)

third_fridays = {}
for month in set(vstoxx_futures["EXP_MONTH"]):
    third_fridays[month]= third_friday(dt(2014, month,1)) 


pricing_date = dt(2014, 3, 31)
maturity = third_fridays[10]
initial_value = vstoxx_index["V2TX"][pricing_date]
forward = vstoxx_futures[(vstoxx_futures.DATE==pricing_date) 
                    & (vstoxx_futures.MATURITY==maturity)]["PRICE"].values[0]
data = {
    "DATE":pricing_date, 
    "EXP_YEAR":maturity.year, 
    "EXP_MONTH":10, 
    "TYPE":"C",
	"STRIKE":[17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0], 
	"PRICE":[4.85, 4.30, 3.80, 3.40, 3.05, 2.75, 2.50, 2.25, 2.10],
	"MATURITY":maturity
}

option_selection = pd.DataFrame(data)

me_vstoxx = market_enviroment("me_vstoxx", pricing_date)
me_vstoxx.add_constant("initial_value", initial_value)
me_vstoxx.add_constant("final_date", maturity)
me_vstoxx.add_constant("currency", "EUR")
me_vstoxx.add_constant("frequency", "B")
me_vstoxx.add_constant("paths", 10000)
csr = short_rate("csr", 0.01)
me_vstoxx.add_curve("discount_curve", csr)

"""
The main aim of calibrating the square root deffusion model is to find optimal param values for 
kappa, theta and volatility.
"""

me_vstoxx.add_constant("kappa", 1.0)
me_vstoxx.add_constant("theta", 1.2*initial_value)
vol_est = vstoxx_index["V2TX"].std()*np.sqrt(len(vstoxx_index["V2TX"])/252.0)
me_vstoxx.add_constant("volatility", vol_est)
vstoxx_model = square_root_deffusion("vstoxx_model", me_vstoxx)

me_vstoxx.add_constant("strike", forward)
me_vstoxx.add_constant("maturity", maturity)

payoff_func = "np.maximum(maturity_value - strike, 0)"
vstoxx_eur_call = european_valuation("vstox_european_call", vstoxx_model, me_vstoxx, payoff_func)
print(vstoxx_eur_call.present_value())

option_models = {}
for option in option_selection.index:
	strike = option_selection["STRIKE"].iloc[option]
	me_vstoxx.add_constant("strike", strike)
	option_models[option] = \
	            european_valuation(
	            	"eur_call_%d" % strike, 
	            	vstoxx_model,
	            	me_vstoxx,
	            	payoff_func)
def calculate_model_values(p0):
	"""
	returns al relevent option values
	"""
	kappa, theta, volatility = p0
	vstoxx_model.update(kappa=kappa, theta=theta, volatility=volatility)
	model_values = {}
	for option in option_models:
		model_values[option] = option_models[option].present_value(fixed_seed=True)
	return model_values

#model_values = calculate_model_values((0.5, 27.5, vol_est))
i=0
def mean_square_error(p0):
	"""
	returns mse given the model and market values 
	"""
	global i 
	#model_values = np.array(calculate_model_values(p0).values())
	model_values = [value for value in calculate_model_values(p0).values()]
	market_values = option_selection["PRICE"].values
	option_diffs = model_values - market_values
	MSE = np.sum(option_diffs**2)/len(option_diffs)

	if i % 20 == 0:
		if i == 0:
			print("%4s %6s %6s -%6s --> %6s" % ("i", "kappa", "theta", "vola", "MSE"))
		print("%4d %6.3f %6.3f %6.3f --> %6.3f" % (i, p0[0], p0[1], p0[2], MSE))
	i += 1
	return MSE

#mse = mean_square_error((0.5,27.5,vol_est))
i=0
opt_global = spo.brute(mean_square_error, 
	((0.5, 3.01, 0.5),
	 (15.0, 30.1, 5.0),
	 (0.5, 5.51, 1))
	, finish=None)

i=0
mse_global = mean_square_error(opt_global)
print(mse_global)


i=0
opt_local = spo.fmin(mean_square_error, opt_global, xtol=0.00001, ftol=0.00001, maxiter=100, maxfun=350)

i=0
mse_local = mean_square_error(opt_local)
print(mse_local)

model_values = calculate_model_values(opt_local)
print(model_values)
				
option_selection["MODEL"] = [value for value in calculate_model_values(opt_local).values()]
option_selection["ERRORS"] = option_selection["MODEL"] - option_selection["PRICE"]
print(option_selection[["MODEL", "PRICE", "ERRORS"]])
print(round(option_selection["ERRORS"].mean(),3))"""