import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import ExternalFactors
from heatpro.temporal_demand import MonthlyHeatDemand, YearlyHeatDemand

from backend.external_factors import plot_external_factors, plot_induced_factors
import backend.factors as fc
import backend.industry as ind
import backend.residential as res
import backend.hot_water as hw
import backend.soil as sl
from backend.pipeline import calculate_induced_factors, process_hot_water_temporal_demand, process_residential_temporal_demand, process_industry_temporal_demand, process_loss_temporal_demand
from backend.visualisation import plot_generated_load

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 1500px !important; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)
with open('logo/heatpro_app_logo.txt', 'r') as f:
    heatpro_app_logo = f.read()
st.markdown(heatpro_app_logo,unsafe_allow_html=True)
st.markdown("<h3>Streamlit App based on <a href='https://github.com/CEA-Liten/HeatPro'>HeatPro</a></h3>", unsafe_allow_html=True)

with st.sidebar:
    with open('logo/CEA_LITEN_logo.txt', 'r') as f:
        cea_logo = f.read()
    st.markdown(cea_logo,unsafe_allow_html=True)
    
    meta_tabs = st.tabs([
            "☔ Factors",
            "🏘️ Residential",
            "♨️ Hot Water",
            "🏭 Industry",
            "🌍 Soil",
        ])
    
    with meta_tabs[0]: # ☔ External Factors
            
        external_factors_file = st.file_uploader("External Factors CSV")
        
        if external_factors_file is not None:
            external_factors = ExternalFactors(pd.read_csv(external_factors_file,index_col=0,parse_dates=True))
            month_index = external_factors.data.resample('MS').sum().index
            year_index = external_factors.data.resample('YS').sum().index
            
        st.subheader("Temperature Departure")
        T_departure = fc.set_temperature_departure_board()
        st.subheader("Temperature Return")
        T_return = fc.set_temperature_return_board() 
        st.subheader("Temperature difference")
        delta_temperature = fc.set_temperature_difference_board()
        
                    
    with meta_tabs[1]: # 🏘️ Residential
        non_heating_temperature = st.number_input("Non-Heating Temperature",value=18.)
        
        st.subheader("Monthly Heat Demand including Hot Water")
        try:
            monthly_building_load_df = st.data_editor(res.generate_default_monthly_building_load(month_index))
            st.plotly_chart(res.plot_monthly_building_load(monthly_building_load_df),use_container_width=True)
            weekly_non_normalized_residential_profile = st.data_editor(res.generate_default_residential_profile())
            st.plotly_chart(res.plot_weekly_residential_profile(weekly_non_normalized_residential_profile),use_container_width=True)
        except NameError:
            st.write("☔ External Factors not received")
        
    with meta_tabs[2]: # ♨️ Hot Water
        hot_water = hw.set_hot_water_config()
        st.subheader("Monthly Sociological Hot Water Profile")
        
        try:
            monthly_hotwater_non_normalized = st.data_editor(hw.generate_monthly_hotwater_profile(month_index))
            st.plotly_chart(hw.plot_monthly_hotwater_profile(monthly_hotwater_non_normalized),use_container_width=True)
            weekly_hot_water_non_normalized = st.data_editor(hw.generate_weekly_hotwater_profile())
            st.plotly_chart(hw.plot_weekly_hot_water_profile(weekly_hot_water_non_normalized),use_container_width=True)
        
            monthly_hot_water_profile = monthly_hotwater_non_normalized / monthly_hotwater_non_normalized.sum()
        except NameError:
            st.write("☔ External Factors not received")
        
    with meta_tabs[3]: # 🏭 Industry
        st.header("Yearly Heat Demand")
        try:
            yearly_industry_consumption = st.data_editor(ind.generate_default_yearly_industry_demand(year_index))
            weekly_industry_profile = st.data_editor(ind.generate_weekly_industry_profile())
            st.plotly_chart(ind.plot_weekly_industry_profile(weekly_industry_profile),use_container_width=True)
        except NameError:
            st.write("☔ External Factors not received")
        
    with meta_tabs[4]: # 🌍 Soil
        soil = sl.set_soil_temperature_board()
        
try:
    induced_factors = calculate_induced_factors(external_factors,T_departure,T_return,soil)
    
    monthly_building_load = MonthlyHeatDemand("residential",monthly_building_load_df)
    
    hourly_hot_water_load = process_hot_water_temporal_demand(monthly_building_load,monthly_hot_water_profile,weekly_hot_water_non_normalized,external_factors,hot_water)
    
    monthly_residential_load = MonthlyHeatDemand('building',(monthly_building_load.data - hourly_hot_water_load.data.resample('MS').sum()))
    hourly_residential_load = process_residential_temporal_demand(external_factors,monthly_residential_load,non_heating_temperature,weekly_non_normalized_residential_profile)

    yearly_industry_load = YearlyHeatDemand("industry",yearly_industry_consumption)
    hourly_industry_load = process_industry_temporal_demand(yearly_industry_load,external_factors,weekly_industry_profile)

    yearly_heat_loss_load = YearlyHeatDemand('heat_loss',pd.DataFrame([20_000_000] * len(year_index),columns=[ENERGY_FEATURE_NAME],index=year_index,))
    hourly_heat_loss_load = process_loss_temporal_demand(induced_factors,yearly_heat_loss_load)

    district_heating = DistrictHeatingLoad(
                                demands = [
                                    hourly_hot_water_load,
                                    hourly_industry_load,
                                    hourly_heat_loss_load,
                                    hourly_residential_load,
                                ],
                                external_factors=external_factors,
                                district_network_temperature=induced_factors,
                                delta_temperature=delta_temperature,
                                cp=soil.capacity,
                            )
    if st.button("Fit District Heating Temperature"):
        district_heating.fit()
except NameError:
    district_heating = None

with st.expander("External and Induced Factors",expanded=True):
    if district_heating:  
        st.plotly_chart(plot_external_factors(district_heating),use_container_width=True)
        
        st.plotly_chart(plot_induced_factors(district_heating),use_container_width=True)
    else:
        st.write("☔ External Factors not received")
        
with st.expander("Generated Load",expanded=True):
    if district_heating:  
        
        st.plotly_chart(plot_generated_load(district_heating),use_container_width=True)
    else:
        st.write("☔ External Factors not received")
        

