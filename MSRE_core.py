#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:28:06 2021

@author: martin
"""

import MSRE_salts
from scipy import special
import numpy as np
import matplotlib.pyplot as plt

fuel_salt = MSRE_salts.fuel_salt
coolant_salt = MSRE_salts.coolant_salt

def InchesToCm(x):
    return x*2.54

def psigToMPa(x): # psig is relative to ambient pressure of 14.7 psia (absolute)
    return (x+14.7)*6.894757E-3

def GPMtoLitersPerSecond(x):
    return x*6.30901964E-2

def FahrenheitToKelvin(T_F):
    return (T_F-32)*5/9 + 273.15

class CoreParameters():
    def __init__(self):
        self.fuel_salt = MSRE_salts.fuel_salt
        self.graphite_radius_inches = 55.25# MSRE Design and Operation I, Table 5.2
        self.graphite_height_inches = 63.5 # Fig. 5.6
        self.maximum_He_pressure_in_pump_bowl_psig = 25 # # MSRE Design and Operation VI REV3
        self.vessel_inner_radius_inches = 58/2 # MSRE Design and Operation I, Table 5.2
        self.vessel_inner_height_inches = 68
        self.extrapolated_radius_inches = 29.5 # MSRE Design and Operation I, Table 5.4 
        self.extrapolated_height_inches = 78 # -||-
        self.flow_rate_offcenter_channel_gpm = 1
        self.flow_rate_center_channel_gpm = 3
        self.inlet_temperature_F = 1175
        self.outlet_temperature_F = 1225
        self.core_volume_flow_rate_l_per_s = 75.7 # l/s
        self.core_mass_flow_rate_kg_per_s = self.core_volume_flow_rate_l_per_s*self.fuel_salt.density_g_per_cm3
        
        self.graphite_radius_cm = InchesToCm((self.graphite_radius_inches))
        self.graphite_height_cm = InchesToCm((self.graphite_height_inches))
        self.maximum_He_pressure_in_pump_bowl_MPa = psigToMPa(self.maximum_He_pressure_in_pump_bowl_psig)
        self.vessel_inner_radius_cm = InchesToCm(self.vessel_inner_radius_inches)
        self.vessel_inner_height_cm = InchesToCm(self.vessel_inner_height_inches)
        self.extrapolated_radius_cm = InchesToCm(self.extrapolated_radius_inches)
        self.extrapolated_height_cm = InchesToCm(self.extrapolated_height_inches)
        self.flow_rate_offcenter_channel_lps = GPMtoLitersPerSecond(self.flow_rate_offcenter_channel_gpm)
        self.flow_rate_center_channel_lps = GPMtoLitersPerSecond(self.flow_rate_center_channel_gpm)        
        self.inlet_temperature_K = FahrenheitToKelvin(self.inlet_temperature_F)
        self.outlet_temperature_K = FahrenheitToKelvin(self.outlet_temperature_F)
        
        self.thermal_power_MW = 8.00 #
        self.j01 = special.jn_zeros(0,1)
        self.peak_power_density = self.j01/4 * self.thermal_power_MW/(self.extrapolated_height_cm*self.extrapolated_radius_cm*self.vessel_inner_radius_cm*special.j1(self.j01*self.vessel_inner_radius_cm/self.extrapolated_radius_cm)*np.sin(np.pi/2*self.vessel_inner_height_cm/self.extrapolated_height_cm))*1E6 # W/cm**3
        self.average_power_density = self.thermal_power_MW/(self.vessel_inner_radius_cm**2*np.pi*self.vessel_inner_height_cm)*1E6
        self.A_collect_cm2 = 12.903 # cm**2
        self.A_channel_cm2 = 2.875 # cm**2
        self.average_power_density_in_channel = self.average_power_density*self.A_collect_cm2/self.A_channel_cm2 # W/cm**3
        self.velocity_center_channel_cm_per_s = self.flow_rate_center_channel_lps*1E3/self.A_channel_cm2 # cm/s   
        self.velocity_offcenter_channel_cm_per_s = self.flow_rate_offcenter_channel_lps*1E3/self.A_channel_cm2 # cm/s
        # self.PrintMetricParameters() 
        self.q_0_prime = 2*np.pi*self.peak_power_density*self.vessel_inner_radius_cm*self.extrapolated_radius_cm/self.j01*special.j1(self.j01*self.vessel_inner_radius_cm/self.extrapolated_radius_cm) # J/cm
    def PrintMetricParameters(self):
        print('graphite_radius = {:.2f} cm'.format(self.graphite_radius_cm))
        print('graphite_height = {:.2f} cm'.format(self.graphite_height_cm))
        print('maximum_He_pressure_in_pump_bowl = {:.4f} MPa'.format(self.maximum_He_pressure_in_pump_bowl_MPa))
        print('vessel_inner_radius = {:.2f} cm'.format(self.vessel_inner_radius_cm))
        print('extrapolated_radius = {:.2f} cm'.format(self.extrapolated_radius_cm))
        print('extrapolated_height = {:.2f} cm'.format(self.extrapolated_height_cm))
        
    def PowerDensity(self,r,z):
        power_density = self.peak_power_density*special.j0(self.j01*r/self.extrapolated_radius_cm)*np.cos(np.pi*z/self.extrapolated_height_cm) # W/cm**3
        return power_density
    
    def ChannelEnthalpy(self,r,z,center=True): # r and z in cm
        if center==True:
            v = self.velocity_center_channel_cm_per_s
        else:
            v = self.velocity_offcenter_channel_cm_per_s
        B = self.peak_power_density*self.A_collect_cm2/self.A_channel_cm2*special.j0(self.j01*r/self.extrapolated_radius_cm) # W/cm**3
        enthalpy = B*self.extrapolated_height_cm/(np.pi*v)*(np.sin(np.pi*z/self.extrapolated_height_cm)+np.sin(np.pi*self.vessel_inner_height_cm/(2*self.extrapolated_height_cm)))
        return enthalpy #  J/cm**3
    def AverageEnthalpy(self,z):
        enthalpy = self.q_0_prime*self.extrapolated_height_cm/(self.core_mass_flow_rate_kg_per_s*np.pi)*(np.sin(np.pi*z/self.extrapolated_height_cm)+np.sin(np.pi*self.vessel_inner_height_cm/(2*self.extrapolated_height_cm)))
        return enthalpy # J/kg
cp = CoreParameters()
# Pressure drop: Fig. 5.10 in MSRE Design and Operation I, Table 5.2
# print(core_parameters.PowerDensity(0, 0))

z = np.linspace(-cp.vessel_inner_height_cm/2,cp.vessel_inner_height_cm/2,1000)

enthalpy = cp.AverageEnthalpy(z)
plt.close('all')
fig, ax = plt.subplots(dpi=150,constrained_layout=True)
ax.plot(z,enthalpy)
ax.set_xlabel('z / cm')
ax.set_ylabel('enthalpy increase  /  J kg$^{-1}$')

def enthalpyincrease2T(x):
    return cp.inlet_temperature_K + x/(cp.fuel_salt.heat_capacity_J_per_g_K*1E3)

def T2enthalpyincrease(x):
    return (x-cp.inlet_temperature_K)*cp.fuel_salt.heat_capacity_J_per_g_K*1E3

secax = ax.secondary_yaxis('right', functions=(enthalpyincrease2T, T2enthalpyincrease))
secax.set_ylabel('T / K')
plt.show()

def PlotSingleChannels():
    enthalpy_center = cp.ChannelEnthalpy(0,z,center=True)
    enthalpy_1 = cp.ChannelEnthalpy(4*2.54,z,center=False)
    enthalpy_2 = cp.ChannelEnthalpy(cp.vessel_inner_radius_cm-2.54,z,center=False)
    
    plt.close('all')
    fig,ax = plt.subplots(dpi=150)
    ax.plot(z,enthalpy_center,label='center')
    ax.plot(z,enthalpy_1,label='4 inches off-center')
    ax.plot(z,enthalpy_2,label='circumference')
    ax.set_xlabel('z / cm')
    ax.set_ylabel('enthalpy increase / J cm$^{-3}$')
    leg = fig.legend()
    leg.set_draggable(True)
    
    fuel_salt = MSRE_salts.fuel_salt
    temperature_center = cp.inlet_temperature_K + enthalpy_center/fuel_salt.volumetric_heat_capacity_J_per_cm3_K
    temperature_1 = cp.inlet_temperature_K + enthalpy_1/fuel_salt.volumetric_heat_capacity_J_per_cm3_K
    temperature_2 = cp.inlet_temperature_K + enthalpy_2/fuel_salt.volumetric_heat_capacity_J_per_cm3_K
    fig2,ax2 = plt.subplots(dpi=150)
    ax2.plot(z,temperature_center,label='center')
    ax2.plot(z,temperature_1,label='4 inches off-center')
    ax2.plot(z,temperature_2,label='circumference')
    ax2.set_xlabel('z / cm')
    ax2.set_ylabel('temperature / K')
    leg2 = fig2.legend()
    leg2.set_draggable(True)
    
