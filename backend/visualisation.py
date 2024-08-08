import pandas as pd
import plotly.graph_objects as go

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import HEATING_SEASON_NAME, EXTERNAL_TEMPERATURE_NAME

def plot_generated_load(district_heating: DistrictHeatingLoad) -> go.Figure:
    palette = dict(zip(district_heating.demands.keys(),['rgb(127,179,228,0.6)', 'rgb(254,152,152,0.6)', 'rgb(190,226,253,0.6)', 'rgb(254,212,213,0.6)']))
    names = dict(zip(district_heating.demands.keys(),['Domestic Hot Water', 'Industry', 'Heat Loss', 'Space Heating']))
    fig = go.Figure(
            data=[
                go.Scatter(
                    x = hourly_load.index,
                    y = hourly_load[ENERGY_FEATURE_NAME],
                    name=names[sector],
                    stackgroup="positive",
                    line_width=0,
                    fillcolor=palette[sector],
                ) for sector, hourly_load in district_heating.demands.items()],
            layout_title_text="Hourly Heat Demand",
            layout_yaxis_title='<b>kW</b>',
            layout_legend=dict(
                        orientation="h",
                        yanchor="top",  
                        xanchor="left", 
                        y=-0.1,         
                            ),
            layout_hovermode='x unified',
        )
    
    y_max = float('-inf')
    for trace in fig.data:
        if 'y' in trace:
            y_max = max(y_max, max(trace.y))
    changes = district_heating.external_factors.data[HEATING_SEASON_NAME].diff().astype(bool)
    changing_date = pd.concat((changes[changes == True],changes.tail(1)))
    for start, end in zip(changing_date[::2].index,changing_date[1::2].index):
        fig.add_annotation(
                text="Heating Season",
                x=start,
                y=y_max*1.1,
                font = dict(size=14, color='green'),
                showarrow=False,
                xanchor="left",
            )
        fig.add_vrect(
            x0=start, 
            x1=end,
            line_width=0,
            fillcolor="rgb(108, 150, 116)",
            opacity=0.5,
            layer="below",
            )
    return fig

def plot_monotone(district_heating: DistrictHeatingLoad) -> go.Figure:
    """Plot the heat monotone corresponding to the heat demand"""
    palette = dict(zip(district_heating.demands.keys(),['rgb(127,179,228,0.6)', 'rgb(254,152,152,0.6)', 'rgb(190,226,253,0.6)', 'rgb(254,212,213,0.6)']))
    names = dict(zip(district_heating.demands.keys(),['Domestic Hot Water', 'Industry', 'Heat Loss', 'Space Heating']))
    #sort index 
    sorted_index=pd.concat(
        (
            hourly_load[ENERGY_FEATURE_NAME] for hourly_load in district_heating.demands.values()
        ), axis=1, ignore_index=True
    ).sum(1).sort_values(ascending=False).index
    # Create plot
    fig = go.Figure(
            data=[
                go.Scatter(
                    x = [i/len(hourly_load.index)*100 for i in range(len(hourly_load.index))],
                    y = hourly_load[ENERGY_FEATURE_NAME].reindex(sorted_index),
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
    return fig

def plot_demand_vs_outside_temperature(district_heating: DistrictHeatingLoad) -> go.Figure:
    """Plot a scatter figure of demand versus outside temperature"""
    
    # Extracting data
    demand = pd.concat(
        (hourly_load[ENERGY_FEATURE_NAME] for hourly_load in district_heating.demands.values()), 
        axis=1, ignore_index=True
    ).sum(1)
    
    fig = go.Figure()
    
    # Trace for True values (e.g., during heating season)
    fig.add_trace(
        go.Scatter(
            x=district_heating.external_factors.data[EXTERNAL_TEMPERATURE_NAME][district_heating.external_factors.data[HEATING_SEASON_NAME]],
            y=demand[district_heating.external_factors.data[HEATING_SEASON_NAME]],
            mode="markers",
            marker=dict(
                size=8,
                color="rgb(108, 150, 116)"  # Green color for heating season
            ),
            name="Heating Season"  
        )
    )
    
    # Trace for False values (e.g., outside heating season)
    fig.add_trace(
        go.Scatter(
            x=district_heating.external_factors.data[EXTERNAL_TEMPERATURE_NAME][~district_heating.external_factors.data[HEATING_SEASON_NAME]],
            y=demand[~district_heating.external_factors.data[HEATING_SEASON_NAME]],
            mode="markers",
            opacity=0.5,
            marker=dict(
                size=8,
                color="rgb(13, 117, 194)"  # Blue color for not heating season
            ),
            name="Not during Heating Season"  
        )
    )
    
    # Layout and figure settings
    fig.update_layout(
        title="Temperature effect on demand",
        yaxis_title='<b>Power demand (kW)</b>',
        xaxis_title='<b>Outside temperature (°C)</b>',
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="left",
            y=-0.1,
        ),
        hovermode='x unified',
    )
    
    return fig
