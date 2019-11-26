import datetime as dt 
from short_rate import short_rate
from market_enviroments import market_enviroment

dates = [dt.datetime(2017,1,1), dt.datetime(2017,2,1), dt.datetime(2017,3,1),
dt.datetime(2017,4,1), dt.datetime(2017,5,1), dt.datetime(2017,6,1), dt.datetime(2017,7,1),
dt.datetime(2017,8,1), dt.datetime(2017,9,1),dt.datetime(2017,10,1), 
dt.datetime(2017,11,1), dt.datetime(2017,12,1), dt.datetime(2018,1,1)]

csr = short_rate('csr', 0.05)
discount_factors = csr.get_discount_factors(dates)
print(discount_factors)

mar_env = market_enviroment("test_env", dates[0])
mar_env.add_constant("drift", 0.1)
mar_env.add_constant("vol", 0.2)
mar_env.add_constant("deffusion", 0.3)
mar_env.add_curve("shor_rate", csr)
mar_env.add_list("dates",discount_factors)



