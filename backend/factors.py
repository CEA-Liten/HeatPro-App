import streamlit as st

from config import TemperatureDeparture, TemperatureReturn

def set_temperature_departure_board() -> TemperatureDeparture:
    col1, col2 = st.columns(2)
    with col1:
        T_max_HS = st.number_input("Max temperature departure heating season (°C)",min_value=0.,value=90.)
        T_max_NHS = st.number_input("Max temperature departure non-heating season (°C)",min_value=0.,value=75.)
        T_ext_mid = st.number_input("External temperature middle threshold (°C)",value=15.)
    with col2:
        T_min_HS = st.number_input("Min temperature departure heating season (°C)",min_value=0.,value=70.)
        T_min_NHS = st.number_input("Min temperature departure non-heating season (°C)",min_value=0.,value=68.)
        T_ext_min = st.number_input("External temperature minimum threshold (°C)",value=-15.)
    return TemperatureDeparture(T_max_HS,T_max_NHS,T_min_HS,T_min_NHS,T_ext_mid,T_ext_min)
    
def set_temperature_return_board() -> TemperatureReturn:
    col1, col2 = st.columns(2)
    with col1:
        T_HS = st.number_input("Temperature return heating season (°C)",min_value=0.,value=50.)
    with col2:
        T_NHS = st.number_input("Temperature return non-heating season (°C)",min_value=0.,value=55.)
    return TemperatureReturn(T_HS,T_NHS)

def set_temperature_difference_board() -> float:
    delta_temperature = st.number_input("External temperature minimum threshold (°C)",min_value=0.,value=7.)
    return delta_temperature