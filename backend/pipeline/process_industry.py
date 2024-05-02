import pandas as pd

from heatpro.check import WEIGHT_NAME_REQUIRED
from heatpro.demand_profile import apply_weekly_hourly_pattern,month_length_proportionnal_weight, day_length_proportionnal_weight
from heatpro.disaggregation import weekly_weighted_disaggregate, monthly_weighted_disaggregate
from heatpro.external_factors import ExternalFactors
from heatpro.temporal_demand import YearlyHeatDemand, HourlyHeatDemand

from backend import DAY_NUMBERS

def process_industry_temporal_demand(yearly_industry_load: YearlyHeatDemand, external_factors: ExternalFactors, weekly_industry_profile:pd.DataFrame) -> HourlyHeatDemand:
    monthly_industry_load = monthly_weighted_disaggregate(
                                                                    yearly_demand=yearly_industry_load,
                                                                    weights = month_length_proportionnal_weight(pd.date_range('2021',end='2022',freq='MS',inclusive='left'))
                                                                )

    return weekly_weighted_disaggregate(
                                    monthly_demand=monthly_industry_load,
                                    weights=apply_weekly_hourly_pattern(
                                        hourly_index=external_factors.data.index,
                                        hourly_mapping={(DAY_NUMBERS[row['day']],row['hour']):row[WEIGHT_NAME_REQUIRED]/weekly_industry_profile.query(f"day=='{row['day']}'")[WEIGHT_NAME_REQUIRED].sum()
                                                        for _, row in weekly_industry_profile.iterrows()}
                                        )*\
                                        day_length_proportionnal_weight(dates=external_factors.data.index),
                                )