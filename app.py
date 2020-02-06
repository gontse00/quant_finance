import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_table as d_table
from dash.exceptions import PreventUpdate
from datetime import datetime as dt
import pandas as pd
import numpy as np

from simulation.geometric_brownian_motion import geometric_brownian_motion
from simulation.jump_deffusion import jump_deffusion
from simulation.square_root_deffusion import square_root_deffusion

from frame import short_rate, market_enviroment, year_fractions

app = dash.Dash(__name__, meta_tags=[{"name":"viewpoint", "content":"width-device-width"}])
app.layout = \
html.Div(
    className="row",
    children=[
        html.Div(
            className="nine columns div-left-panel",
            children=[
                html.H6(children="EURO STOXX 50 Volatility(VSTOXX) EUR Price .V2TX last 60.89")])]
    )

if __name__=='__main__':
    app.run_server(debug=True)
