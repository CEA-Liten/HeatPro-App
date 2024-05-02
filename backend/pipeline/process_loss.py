import pandas as pd

from heatpro.check import ENERGY_FEATURE_NAME
from heatpro.demand_profile import Y_to_H_thermal_loss_profile
from heatpro.temporal_demand import HourlyHeatDemand, YearlyHeatDemand

def process_loss_temporal_demand(induced_factors: pd.DataFrame, yearly_heat_loss_load: YearlyHeatDemand) -> HourlyHeatDemand:
    return HourlyHeatDemand(
                                'heat_loss',
                                (Y_to_H_thermal_loss_profile(induced_factors) * yearly_heat_loss_load.data[ENERGY_FEATURE_NAME].iloc[0]).rename(columns={'weight':ENERGY_FEATURE_NAME})
                            )