import pandas as pd

from backend import DAY_NUMBERS
import config

from heatpro.check import WEIGHT_NAME_REQUIRED
from heatpro.demand_profile import apply_weekly_hourly_pattern, basic_hot_water_hourly_profile
from heatpro.external_factors import ExternalFactors
from heatpro.temporal_demand import MonthlyHeatDemand, HourlyHeatDemand
from heatpro.special_hot_water import special_hot_water

def process_hot_water_temporal_demand(monthly_building_load: MonthlyHeatDemand, monthly_hot_water_profile: pd.DataFrame, weekly_hot_water_non_normalized: pd.DataFrame, external_factors: ExternalFactors, config_hot_water: config.HotWater) -> HourlyHeatDemand:
    return special_hot_water(
                external_factors=external_factors,
                total_heating_including_hotwater=monthly_building_load,
                monthly_hot_water_profile=monthly_hot_water_profile,
                temperature_hot_water=config_hot_water.temperature,
                hourly_hot_water_day_profil = basic_hot_water_hourly_profile(
                                                        raw_hourly_hotwater_profile = apply_weekly_hourly_pattern(
                                                            hourly_index=external_factors.data.index,
                                                            hourly_mapping={(DAY_NUMBERS[row['day']],row['hour']):row[WEIGHT_NAME_REQUIRED]/weekly_hot_water_non_normalized.query(f"day=='{row['day']}'")[WEIGHT_NAME_REQUIRED].sum()
                                                                            for _, row in weekly_hot_water_non_normalized.iterrows()}
                                                            ),
                                                        simultaneity=config_hot_water.simultaneity,
                                                        sanitary_loop_coef=config_hot_water.sanitary_loop_coef,
                                                            )
                                        )