"""import datetime as dt 
from short_rate import short_rate
from market_enviroments import market_enviroment"""
import datetime as dt 
from frame import short_rate, market_enviroment, year_fractions
from random_number_generator.standard_normal_rn import standard_normal_rn 
from simulation.geometric_brownian_motion import *
from simulation.jump_deffusion import *

dates = [dt.datetime(2017,1,1), dt.datetime(2017,2,1), dt.datetime(2017,3,1),
dt.datetime(2017,4,1), dt.datetime(2017,5,1), dt.datetime(2017,6,1), dt.datetime(2017,7,1),
dt.datetime(2017,8,1), dt.datetime(2017,9,1),dt.datetime(2017,10,1), 
dt.datetime(2017,11,1), dt.datetime(2017,12,1), dt.datetime(2018,1,1)]

deltals = year_fractions(dates)
csr = short_rate('csr', 0.05)
discount_factors = csr.get_discount_factors(dates)
#print(discount_factors)

mar_env = market_enviroment("test_env", dates[0])
mar_env.add_constant("drift", 0.1)
mar_env.add_constant("vol", 0.2)
mar_env.add_constant("deffusion", 0.3)
mar_env.add_curve("shor_rate", csr)
mar_env.add_list("dates",discount_factors)

snrn = standard_normal_rn((1,5,len(dates)))
#print(snrn)

me_gbm = market_enviroment("me_gbm", dt.datetime(2019,11,26))
me_gbm.add_constant("initial_value", 36.)
me_gbm.add_constant("volatility", 0.2)
me_gbm.add_constant("final_date", dt.datetime(2020,11,26))
me_gbm.add_constant("frequency", "B")
me_gbm.add_constant("currency", "ZAR")
me_gbm.add_constant("paths", 10000)
me_gbm.add_curve("discount_curve", csr)

#gbm = geometric_brownian_motion("gbm", me_gbm)
#gbm.generate_time_grid()
#paths1 = gbm.get_instrument_values()

me_jump = market_enviroment("jump_env", dt.datetime(2019,11,26))
me_jump.add_enviroment(me_gbm)
me_jump.add_constant("lambda", 0.8)
me_jump.add_constant("mu", -0.25)
me_jump.add_constant("delta", 0.1)

jd = jump_deffusion("jd",me_jump)
jd.generate_time_grid()
paths2 = jd.get_instrument_values()


import matplotlib.pyplot as plt 
plt.plot(jd.time_grid, paths2[:,:10])
plt.show()