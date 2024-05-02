import pandas as pd

from heatpro.external_factors import ExternalFactors
from heatpro.external_factors import closed_heating_season, burch_cold_water, basic_temperature_departure, basic_temperature_return, kasuda_soil_temperature

import config

def calculate_induced_factors(external_factors: ExternalFactors, T_departure: config.TemperatureDeparture, T_return: config.TemperatureReturn, soil:config.Soil) -> pd.DataFrame:
    return pd.concat((
                    closed_heating_season(external_factors),
                    burch_cold_water(external_factors),
                    basic_temperature_departure(external_factors,
                                                T_max_HS=T_departure.max_HS,
                                                T_max_NHS=T_departure.max_NHS,
                                                T_min_HS=T_departure.min_HS,
                                                T_min_NHS=T_departure.min_NHS,
                                                T_ext_mid=T_departure.ext_mid,
                                                T_ext_min=T_departure.ext_min,
                                                ),
                    basic_temperature_return(external_factors,
                                                T_HS=T_return.HS,
                                                T_NHS=T_return.NHS,
                                                ),
                    kasuda_soil_temperature(external_factors,
                                            d=soil.depth,
                                            alpha=soil.conductivity*24*3600/(soil.capacity*soil.density)
                                            ),
                        )
                        ,axis=1)