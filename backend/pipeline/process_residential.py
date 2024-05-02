import pandas as pd

from heatpro.check import WEIGHT_NAME_REQUIRED
from heatpro.external_factors import ExternalFactors, EXTERNAL_TEMPERATURE_NAME
from heatpro.demand_profile import apply_weekly_hourly_pattern, basic_building_heating_profile, BUILDING_FELT_TEMPERATURE_NAME
from heatpro.disaggregation import weekly_weighted_disaggregate
from heatpro.temporal_demand import HourlyHeatDemand, MonthlyHeatDemand

from backend import DAY_NUMBERS

def process_residential_temporal_demand(external_factors: ExternalFactors, monthly_residential_load: MonthlyHeatDemand,non_heating_temperature: float, weekly_non_normalized_residential_profile: pd.DataFrame) -> HourlyHeatDemand:
    hourly_residential_profile = basic_building_heating_profile(
                    felt_temperature=pd.DataFrame(external_factors.data[EXTERNAL_TEMPERATURE_NAME].ewm(24).mean().rename(BUILDING_FELT_TEMPERATURE_NAME)),
                    non_heating_temperature=non_heating_temperature,
                    hourly_weight=apply_weekly_hourly_pattern(
                        hourly_index=external_factors.data.index,
                        hourly_mapping={(DAY_NUMBERS[row['day']],row['hour']):row[WEIGHT_NAME_REQUIRED]
                                        for _, row in weekly_non_normalized_residential_profile.iterrows()}
                    )
                )

    return weekly_weighted_disaggregate(
                                    monthly_demand=monthly_residential_load,
                                    weights=hourly_residential_profile,
                                )