import pandas as pd
import plotly.graph_objects as go

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import HEATING_SEASON_NAME

def plot_generated_load(district_heating: DistrictHeatingLoad) -> go.Figure:
    fig = go.Figure(
            data=[
                go.Scatter(
                    x = hourly_load.index,
                    y = hourly_load[ENERGY_FEATURE_NAME],
                    name=sector,
                    stackgroup="positive",
                    line_width=0,
                ) for sector, hourly_load in district_heating.demands.items()]
        )
    y_max = float('-inf')
    for trace in fig.data:
        if 'y' in trace:
            y_max = max(y_max, max(trace.y))
    fig.add_annotation(
        text="Non Heating Season",
        x=district_heating.external_factors.data[~district_heating.external_factors.data[HEATING_SEASON_NAME]].index.min(),
        y=y_max*1.1,
        font = dict(size=14, color='black'),
        showarrow=False,
        yanchor="top",
        xanchor="left",
    )
    fig.add_vrect(
        x0=district_heating.external_factors.data[~district_heating.external_factors.data[HEATING_SEASON_NAME]].index.min(), 
        x1=district_heating.external_factors.data[~district_heating.external_factors.data[HEATING_SEASON_NAME]].index.max(),
        line_width=0,
        fillcolor='orange',
        opacity=0.5,
        layer="below",
        )
    return fig