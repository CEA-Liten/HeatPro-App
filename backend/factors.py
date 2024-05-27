import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import TemperatureDeparture, TemperatureReturn

def set_temperature_departure_board() -> TemperatureDeparture:
    col1, col2 = st.columns(2)
    with col1:
        T_max_HS = st.number_input("Max supply temperature space heating season (°C)",min_value=0.,value=90.,step=1.)
        T_max_NHS = st.number_input("Max supply temperature non-space heating season (°C)",min_value=0.,value=75.,step=1.)
        T_ext_mid = st.number_input("Outside air non-heating temperature (°C)",value=18.,step=1.)
    with col2:
        T_min_HS = st.number_input("Min supply temperature space heating season (°C)",min_value=0.,value=70.,step=1.)
        T_min_NHS = st.number_input("Min supply temperature non-space heating season (°C)",min_value=0.,value=68.,step=1.)
        T_ext_min = st.number_input("Outside air design temperature (°C)",value=-15.,step=1.)
    return TemperatureDeparture(T_max_HS,T_max_NHS,T_min_HS,T_min_NHS,T_ext_mid,T_ext_min)
    
def set_temperature_return_board() -> TemperatureReturn:
    col1, col2 = st.columns(2)
    with col1:
        T_HS = st.number_input("Return temperature space heating season (°C)",min_value=0.,value=50.,step=1.)
    with col2:
        T_NHS = st.number_input("Return temperature non-space heating season (°C)",min_value=0.,value=55.,step=1.)
    return TemperatureReturn(T_HS,T_NHS)

def set_temperature_difference_board() -> float:
    delta_temperature = st.number_input("Maximum return temperature variation with respect to nominal condition (°C)",min_value=0.,value=7.,step=1.)
    return delta_temperature

def plot_supply_temperature(T_departure: TemperatureDeparture) -> go.Figure:
    return go.Figure(
            [go.Scatter(
                x = [T_departure.ext_min,T_departure.ext_mid,25],
                y = [T_departure.max_HS,T_departure.min_HS,T_departure.min_HS],
                name="Heating season",
            ),
             go.Scatter(
                x = [T_departure.ext_min,T_departure.ext_mid,25],
                y = [T_departure.max_NHS,T_departure.min_NHS,T_departure.min_NHS],
                name="Non-heating season",
            ),],
            layout_yaxis_title='Supply temperature (<b>°C</b>)',
            layout_xaxis_title='Outside temperature (<b>°C</b>)',
            layout_legend=dict(
                        orientation="h",
                        yanchor="top",  
                        xanchor="left", 
                        y=-0.2,         
                            )
        )
    