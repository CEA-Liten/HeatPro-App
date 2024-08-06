import pandas as pd
import plotly.graph_objects as go

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import HEATING_SEASON_NAME

def plot_monotone(district_heating: DistrictHeatingLoad) -> go.Figure:
    """Plot the heat monotone corresponding to the heat demand"""
    palette = dict(zip(district_heating.demands.keys(),['rgb(127,179,228,0.6)', 'rgb(254,152,152,0.6)', 'rgb(190,226,253,0.6)', 'rgb(254,212,213,0.6)']))
    names = dict(zip(district_heating.demands.keys(),['Domestic Hot Water', 'Industry', 'Heat Loss', 'Space Heating']))
    fig = go.Figure(
            data=[
                go.Scatter(
                    x = [i/len(hourly_load.index)*100 for i in range(len(hourly_load.index))],
                    y = hourly_load[ENERGY_FEATURE_NAME].sort_values(ascending=False).reset_index(drop=True),
                    name=names[sector],
                    stackgroup="positive",
                    line_width=0,
                    fillcolor=palette[sector],
                ) for sector, hourly_load in district_heating.demands.items()],
            layout_title_text="Ordered Heat Demand",
            layout_yaxis_title='<b>kW</b>',
            layout_xaxis_title='<b>Ordered Hours (%)</b>',
            layout_legend=dict(
                        orientation="h",
                        yanchor="top",  
                        xanchor="left", 
                        y=-0.2,         
                            ),
            layout_hovermode='x unified',
        )
    # Calculate max y
    y_max = float('-inf')
    for trace in fig.data:
        if 'y' in trace:
            y_max = max(y_max, max(trace.y))
    # Color Heating season
    # Calculate changes in heating Season status        
    changes = sorted(district_heating.external_factors.data[HEATING_SEASON_NAME],reverse=True)
    # Find the index where it changes from True to False
    change_index = None
    for i, value in enumerate(changes):
        if  not value:  # if value is False
            change_index = i
            break
    # Add annotation of the period
    fig.add_annotation(
            text="Heating season",
            x=0,
            y=y_max*1.1,
            font = dict(size=14, color='green'),
            showarrow=False,
            xanchor="left",
        )
    # Add a rectangle representing the period
    fig.add_vrect(
        x0=0, 
        x1=change_index,
        line_width=0,
        fillcolor="rgb(108, 150, 116)",
        opacity=0.5,
        layer="below",
        )
    return fig