import pandas as pd

from heatpro.district_heating_load import DistrictHeatingLoad

def ending_dataframe(district_heating: DistrictHeatingLoad, water_heat_capacity: float) -> pd.DataFrame:
    
    features_to_keep = ["external_temperature","heating_season","cold_water_temperature","departure_temperature","return_temperature","soil_temperature","industry_thermal_energy_kWh","hot_water_thermal_energy_kWh","heat_loss_thermal_energy_kWh","building_thermal_energy_kWh"]
    columns_in_order = ["outside_temperature_C","supply_temperature_C","return_temperature_C","flow_rate_m3_h","total_thermal_energy_kWh","heating_season","cold_water_temperature_C","ground_temperature_C","building_thermal_energy_kWh","DHW_thermal_energy_kWh","industry_thermal_energy_kWh","heat_loss_thermal_energy_kWh"]
    return pd.concat(
        (
            district_heating.data[features_to_keep].rename(columns={
                "external_temperature":"outside_temperature_C",
                "cold_water_temperature":"cold_water_temperature_C",
                "departure_temperature":"supply_temperature_C",
                "return_temperature":"return_temperature_C",
                "soil_temperature":"ground_temperature_C",
                "hot_water_thermal_energy_kWh":"DHW_thermal_energy_kWh"
                }),
            district_heating.data[["industry_thermal_energy_kWh","hot_water_thermal_energy_kWh","industry_thermal_energy_kWh","building_thermal_energy_kWh"]].sum(axis=1).rename("total_thermal_energy_kWh"),
            (district_heating.data[["industry_thermal_energy_kWh","hot_water_thermal_energy_kWh","industry_thermal_energy_kWh","building_thermal_energy_kWh"]].sum(axis=1)/water_heat_capacity/(district_heating.data["departure_temperature"]-district_heating.data["return_temperature"])).rename("flow_rate_m3_h")
        ),
        axis=1
    )[columns_in_order]