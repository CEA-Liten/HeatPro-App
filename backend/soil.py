from typing import Tuple

import streamlit as st

from config import Soil

def set_soil_temperature_board() -> Soil:
    col1, col2 = st.columns(2)
    with col1:
        d = st.number_input("Depth (m)",min_value=0.,value=1.)
        dens_ground = st.number_input("Ground density (kg/m3)",min_value=0.,value=3200.)
    with col2:
        capacity_ground = st.number_input("Ground capacity (J/kg/K)",min_value=0.,value=840.)
        conductivity_ground = st.number_input("Ground conductivity (W/m/K)",min_value=0.,value=2.42)
    return Soil(d,dens_ground,capacity_ground,conductivity_ground)