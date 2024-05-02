from dataclasses import dataclass

@dataclass
class TemperatureDeparture:
    max_HS: float
    max_NHS: float
    min_HS: float
    min_NHS: float
    ext_mid: float
    ext_min: float
    
@dataclass
class TemperatureReturn:
    HS: float
    NHS: float
    
@dataclass
class HotWater:
    temperature: float
    simultaneity: float
    sanitary_loop_coef: float
    
@dataclass
class Soil:
    depth: float
    density: float
    capacity: float
    conductivity: float