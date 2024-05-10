import pandas as pd
import plotly.graph_objects as go

from heatpro.external_factors import EXTERNAL_TEMPERATURE_NAME, HEATING_SEASON_NAME
from heatpro.district_heating_load import DistrictHeatingLoad

def plot_external_factors(district_heating: DistrictHeatingLoad) -> go.Figure:
    fig = go.Figure([
            go.Scatter(
                x = district_heating.external_factors.data.index,
                y = district_heating.external_factors.data[EXTERNAL_TEMPERATURE_NAME],
                name = 'External Temperature',
                showlegend=True
            ),
            ],
            layout_title_text="External Factors",
            layout_yaxis_title='<b>°C</b>',
            layout_legend=dict(
                        orientation="h",
                        yanchor="top",  
                        xanchor="left", 
                        y=-0.1,         
                            )
                )
    changes = district_heating.external_factors.data[HEATING_SEASON_NAME].diff().astype(bool).fillna(False)
    changing_date = changes[changes == True][1:]
    for start, end in zip(changing_date[::2].index,changing_date[1::2].index):
        fig.add_annotation(
                text="Non Heating Season",
                x=start,
                y=district_heating.external_factors.data[EXTERNAL_TEMPERATURE_NAME].min(),
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

def plot_induced_factors(district_heating: DistrictHeatingLoad) -> go.Figure:
    fig = go.Figure(
                data=[
                    go.Scatter(
                        x = district_heating.district_network_temperature.index,
                        y = district_heating.district_network_temperature["cold_water_temperature"],
                        name="Cold Water Temperature"
                    ),
                    go.Scatter(
                        x = district_heating.district_network_temperature.index,
                        y = district_heating.district_network_temperature["departure_temperature"],
                        name="Departure Temperature"
                    ),
                    go.Scatter(
                        x = district_heating.district_network_temperature.index,
                        y = district_heating.district_network_temperature["return_temperature"],
                        name="Return Temperature"
                    ),
                    go.Scatter(
                        x = district_heating.district_network_temperature.index,
                        y = district_heating.district_network_temperature["soil_temperature"],
                        name="Soil Temperature"
                    ),
                ],
                layout_title_text="Induced Factors",
                layout_yaxis_title='<b>°C</b>',
                layout_legend=dict(
                            orientation="h",
                            yanchor="top",  
                            xanchor="left", 
                            y=-0.1,         
                                )
            )
        
    changes = district_heating.external_factors.data[HEATING_SEASON_NAME].diff().astype(bool).fillna(False)
    changing_date = changes[changes == True][1:]
    for start, end in zip(changing_date[::2].index,changing_date[1::2].index):
        fig.add_annotation(
                text="Non Heating Season",
                x=start,
                y=district_heating.external_factors.data[EXTERNAL_TEMPERATURE_NAME].min(),
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
    