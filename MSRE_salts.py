#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 09:40:31 2021

@author: martin
"""

class Constants():
    def __init__(self):
        self.btu_to_J = 1055.06
        self.lb_to_g = 453.59237
        self.ft_to_m = 0.3048
        self.Delta_F_to_Delta_K = 5/9
        self.hour_to_s = 60*60

def FahrenheitToCelsius(T_F):
    return (T_F-32)*5/9

def ImperialDensityToMetric(density_lb_per_ft3):
    const = Constants()
    density_g_per_cm3 = const.lb_to_g/(const.ft_to_m*100)**3*density_lb_per_ft3
    return density_g_per_cm3

def ImperialHeatCapacityToJ_per_g_K(heat_capacity_Btu_per_lb_F):
    const = Constants()
    heat_capacity_imperial_to_J_per_g_K = const.btu_to_J/(const.lb_to_g*const.Delta_F_to_Delta_K)
    return heat_capacity_Btu_per_lb_F*heat_capacity_imperial_to_J_per_g_K

def ImperialThermalConductivityTo_W_per_m_K(thermal_conductivity_Btu_per_ft_hr_F):
    const = Constants()
    thermal_conductivity_W_per_m_K = thermal_conductivity_Btu_per_ft_hr_F*const.btu_to_J/(const.ft_to_m*const.hour_to_s*const.Delta_F_to_Delta_K)
    return thermal_conductivity_W_per_m_K

class salt():
    def __init__(self,name,composition,liquidus_temperature_F,physical_properties_temperature_F,density_lb_per_ft3,heat_capacity_Btu_per_lb_F,viscosity_cP,thermal_conductivity_Btu_per_ft_hr_F):
        self.name = name
        self.composition = composition
        self.liquidus_temperature_F = liquidus_temperature_F # degrees F
        self.physical_properties_temperature_F = physical_properties_temperature_F
        self.density_lb_per_ft3 = density_lb_per_ft3
        self.heat_capacity_Btu_per_lb_F = heat_capacity_Btu_per_lb_F
        self.viscosity_cP = viscosity_cP
        self.thermal_conductivity_Btu_per_ft_hr_F = thermal_conductivity_Btu_per_ft_hr_F
        
        self.liquidus_temperature_C = FahrenheitToCelsius(liquidus_temperature_F)
        self.physical_properties_temperature_C = FahrenheitToCelsius(physical_properties_temperature_F)        
        self.density_g_per_cm3 = ImperialDensityToMetric(density_lb_per_ft3)
        self.heat_capacity_J_per_g_K = ImperialHeatCapacityToJ_per_g_K(heat_capacity_Btu_per_lb_F)
        self.viscosity_mPa_s = viscosity_cP
        self.thermal_conductivity_W_per_m_K = ImperialThermalConductivityTo_W_per_m_K(self.thermal_conductivity_Btu_per_ft_hr_F)
    def PrintMetricParameters(self):
        print(self.name)
        print('composition = {}'.format(self.composition))
        print('liquidus_temperature = {:.2f} degree C'.format(self.liquidus_temperature_C))
        print('physical_properties_temperature = {:.2f} degree C'.format(self.physical_properties_temperature_C))
        print('density = {:.3f} g/cm^3'.format(self.density_g_per_cm3))
        print('heat_capacity = {:.3f} J/(g K)'.format(self.heat_capacity_J_per_g_K))
        print('viscosity = {:.3f} mPa s'.format(self.viscosity_mPa_s))
        print('thermal_conductivity = {:.3f} W/(m K)\n'.format(self.thermal_conductivity_W_per_m_K))
        
fuel_salt = salt(name = 'fuel_salt',
                 composition='LiF-BeF2-ZrF4-UF4 (65-29.1-5-0.9 mole %)',
                liquidus_temperature_F = 842,
                physical_properties_temperature_F = 1200,
                density_lb_per_ft3 = 146,
                heat_capacity_Btu_per_lb_F = 0.455,
                viscosity_cP = 7.6,
                thermal_conductivity_Btu_per_ft_hr_F = 3.2,)

coolant_salt = salt(name = 'coolant_salt',
                composition='LiF-BeF2 (66-34 mole %)',
                liquidus_temperature_F = 851,
                physical_properties_temperature_F = 1062,
                density_lb_per_ft3 = 120.5,
                heat_capacity_Btu_per_lb_F = 0.526,
                viscosity_cP = 8.3,
                thermal_conductivity_Btu_per_ft_hr_F = 3.5)

if __name__ == "__main__":
    fuel_salt.PrintMetricParameters()
    coolant_salt.PrintMetricParameters()