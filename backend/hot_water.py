import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from heatpro.check import WEIGHT_NAME_REQUIRED
 
from config import HotWater

def set_hot_water_config() -> HotWater:
    help_simultaneity="""
    The simultaneity coefficient S represents the asynchrony of domestic hot water drawings.

    When this coefficient is equal to 1, there is no excess and the daily energy due to domestic hot water is therefore redistributed according to the standardized profile entered by the user.

    When this coefficient is equal to 0, there is total abundance and the daily energy due to domestic hot water is redistributed equitably for each moment of the day
    """
    temperature_hot_water = st.number_input("Domestic hot water temperature (°C)", value=60.)
    simultaneity = st.number_input("Simultaneity coefficient", value=0.2, help=help_simultaneity)
    sanitary_loop_coef = st.number_input("Domestic hot water loop part (%)", value=30)/100
    return HotWater(temperature_hot_water,simultaneity,sanitary_loop_coef)

def plot_monthly_hotwater_profile(monthly_hotwater_non_normalized: pd.DataFrame) -> go.Figure:
    return go.Figure(
                go.Scatter(
                    x = monthly_hotwater_non_normalized.index,
                    y = monthly_hotwater_non_normalized[WEIGHT_NAME_REQUIRED],
                    name = "Residential heat demand including hot water",
                ),
                layout_yaxis_title = "<b></b>",
                layout_title_text = "Domestic Hot water sociological consumption profile"
            )
    
def plot_weekly_hot_water_profile(weekly_hot_water_non_normalized: pd.DataFrame) -> go.Figure:
    fig =  go.Figure(
                go.Scatter(
                    x = weekly_hot_water_non_normalized.index,
                    y = weekly_hot_water_non_normalized[WEIGHT_NAME_REQUIRED],
                    name = "Domestic hoy water demand profile",
                ),
                layout_yaxis_title = "<b></b>",
                layout_title_text = "Domestic Hot Water demand weekly profile"
            )
    fig.add_vline(x=24, line_color="rgba(0, 0, 0, 0.5)")\
        .add_vline(x=24*2, line_color="rgba(0, 0, 0, 0.5)")\
        .add_vline(x=24*3, line_color="rgba(0, 0, 0, 0.5)")\
        .add_vline(x=24*4, line_color="rgba(0, 0, 0, 0.5)")\
        .add_vline(x=24*5, line_color="rgba(0, 0, 0, 0.5)")\
        .add_vline(x=24*6, line_color="rgba(0, 0, 0, 0.5)")
    return fig
    
def generate_monthly_hotwater_profile(month_index: pd.DatetimeIndex) -> pd.DataFrame:
    return pd.DataFrame(        
                    np.array([1.13,1.11,1.04,1.04,1.0,0.93,0.8,0.74,0.98,1.0,1.09,1.14] * (len(month_index)//12))[:len(month_index)],
                    columns=[WEIGHT_NAME_REQUIRED],
                    index=month_index,
                            )
    
def generate_weekly_hotwater_profile() -> pd.DataFrame:
    return pd.DataFrame(
                                    [ 
                                        ['monday',0,0.408],
                                        ['monday',1,0.216],
                                        ['monday',2,0.12,],
                                        ['monday',3,0.096],
                                        ['monday',4,0.168],
                                        ['monday',5,0.336],
                                        ['monday',6,0.672],
                                        ['monday',7,0.936],
                                        ['monday',8,1.032],
                                        ['monday',9,1.200],
                                        ['monday',10,1.248],
                                        ['monday',11,1.368],
                                        ['monday',12,1.680],
                                        ['monday',13,1.536],
                                        ['monday',14,1.080],
                                        ['monday',15,0.960],
                                        ['monday',16,1.128],
                                        ['monday',17,1.416],
                                        ['monday',18,1.656],
                                        ['monday',19,1.848],
                                        ['monday',20,1.824],
                                        ['monday',21,1.368],
                                        ['monday',22,0.984],
                                        ['monday',23,0.720],
                                        ['tuesday',0,0.408],
                                        ['tuesday',1,0.216],
                                        ['tuesday',2,0.12,],
                                        ['tuesday',3,0.096],
                                        ['tuesday',4,0.168],
                                        ['tuesday',5,0.336],
                                        ['tuesday',6,0.672],
                                        ['tuesday',7,0.936],
                                        ['tuesday',8,1.032],
                                        ['tuesday',9,1.200],
                                        ['tuesday',10,1.248],
                                        ['tuesday',11,1.368],
                                        ['tuesday',12,1.680],
                                        ['tuesday',13,1.536],
                                        ['tuesday',14,1.080],
                                        ['tuesday',15,0.960],
                                        ['tuesday',16,1.128],
                                        ['tuesday',17,1.416],
                                        ['tuesday',18,1.656],
                                        ['tuesday',19,1.848],
                                        ['tuesday',20,1.824],
                                        ['tuesday',21,1.368],
                                        ['tuesday',22,0.984],
                                        ['tuesday',23,0.720],
                                        ['wednesday',0,0.408],
                                        ['wednesday',1,0.216],
                                        ['wednesday',2,0.12,],
                                        ['wednesday',3,0.096],
                                        ['wednesday',4,0.168],
                                        ['wednesday',5,0.336],
                                        ['wednesday',6,0.672],
                                        ['wednesday',7,0.936],
                                        ['wednesday',8,1.032],
                                        ['wednesday',9,1.200],
                                        ['wednesday',10,1.248],
                                        ['wednesday',11,1.368],
                                        ['wednesday',12,1.680],
                                        ['wednesday',13,1.536],
                                        ['wednesday',14,1.080],
                                        ['wednesday',15,0.960],
                                        ['wednesday',16,1.128],
                                        ['wednesday',17,1.416],
                                        ['wednesday',18,1.656],
                                        ['wednesday',19,1.848],
                                        ['wednesday',20,1.824],
                                        ['wednesday',21,1.368],
                                        ['wednesday',22,0.984],
                                        ['wednesday',23,0.720],
                                        ['thursday',0,0.408],
                                        ['thursday',1,0.216],
                                        ['thursday',2,0.12,],
                                        ['thursday',3,0.096],
                                        ['thursday',4,0.168],
                                        ['thursday',5,0.336],
                                        ['thursday',6,0.672],
                                        ['thursday',7,0.936],
                                        ['thursday',8,1.032],
                                        ['thursday',9,1.200],
                                        ['thursday',10,1.248],
                                        ['thursday',11,1.368],
                                        ['thursday',12,1.680],
                                        ['thursday',13,1.536],
                                        ['thursday',14,1.080],
                                        ['thursday',15,0.960],
                                        ['thursday',16,1.128],
                                        ['thursday',17,1.416],
                                        ['thursday',18,1.656],
                                        ['thursday',19,1.848],
                                        ['thursday',20,1.824],
                                        ['thursday',21,1.368],
                                        ['thursday',22,0.984],
                                        ['thursday',23,0.720],
                                        ['friday',0,0.408],
                                        ['friday',1,0.216],
                                        ['friday',2,0.12,],
                                        ['friday',3,0.096],
                                        ['friday',4,0.168],
                                        ['friday',5,0.336],
                                        ['friday',6,0.672],
                                        ['friday',7,0.936],
                                        ['friday',8,1.032],
                                        ['friday',9,1.200],
                                        ['friday',10,1.248],
                                        ['friday',11,1.368],
                                        ['friday',12,1.680],
                                        ['friday',13,1.536],
                                        ['friday',14,1.080],
                                        ['friday',15,0.960],
                                        ['friday',16,1.128],
                                        ['friday',17,1.416],
                                        ['friday',18,1.656],
                                        ['friday',19,1.848],
                                        ['friday',20,1.824],
                                        ['friday',21,1.368],
                                        ['friday',22,0.984],
                                        ['friday',23,0.720],
                                        ['saturday',0,0.432],
                                        ['saturday',1,0.240],
                                        ['saturday',2,0.144],
                                        ['saturday',3,0.120],
                                        ['saturday',4,0.120],
                                        ['saturday',5,0.192],
                                        ['saturday',6,0.312],
                                        ['saturday',7,0.624],
                                        ['saturday',8,0.984],
                                        ['saturday',9,1.416],
                                        ['saturday',10,1.536],
                                        ['saturday',11,1.704],
                                        ['saturday',12,1.800],
                                        ['saturday',13,1.800],
                                        ['saturday',14,1.584],
                                        ['saturday',15,1.200],
                                        ['saturday',16,1.176],
                                        ['saturday',17,1.320],
                                        ['saturday',18,1.488],
                                        ['saturday',19,1.536],
                                        ['saturday',20,1.488],
                                        ['saturday',21,1.176],
                                        ['saturday',22,0.936],
                                        ['saturday',23,0.672],
                                        ['sunday',0,0.360],
                                        ['sunday',1,0.240],
                                        ['sunday',2,0.144],
                                        ['sunday',3,0.096],
                                        ['sunday',4,0.096],
                                        ['sunday',5,0.144],
                                        ['sunday',6,0.192],
                                        ['sunday',7,0.312],
                                        ['sunday',8,0.624],
                                        ['sunday',9,1.080],
                                        ['sunday',10,1.440],
                                        ['sunday',11,1.704],
                                        ['sunday',12,1.824],
                                        ['sunday',13,1.776],
                                        ['sunday',14,1.440],
                                        ['sunday',15,1.272],
                                        ['sunday',16,1.200],
                                        ['sunday',17,1.440],
                                        ['sunday',18,1.824],
                                        ['sunday',19,1.968],
                                        ['sunday',20,1.872],
                                        ['sunday',21,1.368],
                                        ['sunday',22,0.960],
                                        ['sunday',23,0.624],
                                        ],
                                    columns=['day','hour',WEIGHT_NAME_REQUIRED]
                                )