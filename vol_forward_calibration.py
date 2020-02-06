import pandas as pd 
import numpy as np 
import datetime as dt

data = pd.HDFStore("./data/vstoxx_march_2014.h5")
forward_quotes = data["vstoxx_futures"]
forward_quotes = forward_quotes[forward_quotes["DATE"]>=dt.datetime(2014,3,31)]
print(forward_quotes.info())
data.close()
