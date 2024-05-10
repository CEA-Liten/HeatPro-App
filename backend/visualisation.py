import pandas as pd
import plotly.graph_objects as go

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import HEATING_SEASON_NAME

def plot_generated_load(district_heating: DistrictHeatingLoad) -> go.Figure:
    palette = dict(zip(district_heating.demands.keys(),['rgb(127,179,228,0.6)', 'rgb(254,152,152,0.6)', 'rgb(190,226,253,0.6)', 'rgb(254,212,213,0.6)']))
    fig = go.Figure(
            data=[
                go.Scatter(
                    x = hourly_load.index,
                    y = hourly_load[ENERGY_FEATURE_NAME],
                    name=sector,
                    stackgroup="positive",
                    line_width=0,
                    fillcolor=palette[sector],
                ) for sector, hourly_load in district_heating.demands.items()]
        )
    
    y_max = float('-inf')
    for trace in fig.data:
        if 'y' in trace:
            y_max = max(y_max, max(trace.y))
    changes = district_heating.external_factors.data[HEATING_SEASON_NAME].diff().astype(bool).fillna(False)
    changing_date = changes[changes == True][1:]
    for start, end in zip(changing_date[::2].index,changing_date[1::2].index):
        fig.add_annotation(
                text="Non Heating Season",
                x=start,
                y=y_max*1.1,
                font = dict(size=14, color='black'),
                showarrow=False,
                xanchor="left",
            )
        fig.add_vrect(
            x0=start, 
            x1=end,
            line_width=0,
            fillcolor='orange',
            opacity=0.5,
            layer="below",
            )
    return fig