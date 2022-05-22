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

def InchesToCm(x):
    return x*2.54

def psigToMPa(x): # psig is relative to ambient pressure of 14.7 psia (absolute)
    return (x+14.7)*6.894757E-3

def GPMtoLitersPerSecond(x):
    return x*6.30901964E-2

def FahrenheitToKelvin(T_F):
    return (T_F-32)*5/9 + 273.15

class Core():
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
        self.peak_power_density_W_per_cm3 = self.j01/4 * self.thermal_power_MW/(self.extrapolated_height_cm*self.extrapolated_radius_cm*self.vessel_inner_radius_cm*special.j1(self.j01*self.vessel_inner_radius_cm/self.extrapolated_radius_cm)*np.sin(np.pi/2*self.vessel_inner_height_cm/self.extrapolated_height_cm))*1E6 # W/cm**3
        self.average_power_density_W_per_cm3 = self.thermal_power_MW/(self.vessel_inner_radius_cm**2*np.pi*self.vessel_inner_height_cm)*1E6
        self.A_collect_cm2 = 12.903 # cm**2
        self.A_channel_cm2 = 2.875 # cm**2
        self.average_power_density_W_per_cm3_in_channel = self.average_power_density_W_per_cm3*self.A_collect_cm2/self.A_channel_cm2 # W/cm**3
        self.velocity_center_channel_cm_per_s = self.flow_rate_center_channel_lps*1E3/self.A_channel_cm2 # cm/s   
        self.velocity_offcenter_channel_cm_per_s = self.flow_rate_offcenter_channel_lps*1E3/self.A_channel_cm2 # cm/s
        # self.PrintMetricParameters() 
        self.q_0_prime = 2*np.pi*self.peak_power_density_W_per_cm3*self.vessel_inner_radius_cm*self.extrapolated_radius_cm/self.j01*special.j1(self.j01*self.vessel_inner_radius_cm/self.extrapolated_radius_cm) # J/cm
        self.hydrolic_diameter_cm = 4*self.A_channel_cm2/((1.6+0.4*np.pi)*2.54) # cm
        self.reynolds_number_offcenter_channel = self.fuel_salt.density_g_per_cm3*self.velocity_offcenter_channel_cm_per_s*self.hydrolic_diameter_cm/self.fuel_salt.viscosity_mPa_s*1E2
        self.reynolds_number_center_channel = self.fuel_salt.density_g_per_cm3*self.velocity_center_channel_cm_per_s*self.hydrolic_diameter_cm/self.fuel_salt.viscosity_mPa_s*1E2

    def PrintMetricParameters(self):
        print('graphite_radius = {:.2f} cm'.format(self.graphite_radius_cm))
        print('graphite_height = {:.2f} cm'.format(self.graphite_height_cm))
        print('maximum_He_pressure_in_pump_bowl = {:.4f} MPa'.format(self.maximum_He_pressure_in_pump_bowl_MPa))
        print('vessel_inner_radius = {:.2f} cm'.format(self.vessel_inner_radius_cm))
        print('extrapolated_radius = {:.2f} cm'.format(self.extrapolated_radius_cm))
        print('extrapolated_height = {:.2f} cm'.format(self.extrapolated_height_cm))    
    def PowerDensity(self,r,z):
        power_density = self.peak_power_density_W_per_cm3*special.j0(self.j01*r/self.extrapolated_radius_cm)*np.cos(np.pi*z/self.extrapolated_height_cm) # W/cm**3
        return power_density
    def ChannelEnthalpy(self,r,z,center=True): # r and z in cm
        if center==True:
            v = self.velocity_center_channel_cm_per_s
        else:
            v = self.velocity_offcenter_channel_cm_per_s
        mass_flow_rate_kg_per_s = v*self.A_channel_cm2*self.fuel_salt.density_g_per_cm3*1E-3
        q_c0_prime = self.peak_power_density_W_per_cm3*special.j0(self.j01*r/self.extrapolated_radius_cm)*self.A_collect_cm2 # W/cm
        enthalpy = q_c0_prime*self.extrapolated_height_cm/(mass_flow_rate_kg_per_s*np.pi)*(np.sin(np.pi*z/self.extrapolated_height_cm)+np.sin(np.pi*self.vessel_inner_height_cm/(2*self.extrapolated_height_cm)))
        return enthalpy # J/kg
    def GetMaximumPower(self,deltaT,r,center=False):
        if center==True:
            v = self.velocity_center_channel_cm_per_s
        else:
            v = self.velocity_offcenter_channel_cm_per_s
        mass_flow_rate_kg_per_s = v*self.A_channel_cm2*self.fuel_salt.density_g_per_cm3*1E-3
        P_th = deltaT*2*np.pi*self.fuel_salt.heat_capacity_J_per_g_K*1E3*mass_flow_rate_kg_per_s*self.extrapolated_radius_cm*self.vessel_inner_radius_cm/(self.A_collect_cm2*self.j01)*special.j1(self.j01*self.vessel_inner_radius_cm/self.extrapolated_radius_cm)/special.j0(self.j01*r/self.extrapolated_radius_cm)
        return P_th
    def AverageEnthalpy(self,z):
        enthalpy = self.q_0_prime*self.extrapolated_height_cm/(self.core_mass_flow_rate_kg_per_s*np.pi)*(np.sin(np.pi*z/self.extrapolated_height_cm)+np.sin(np.pi*self.vessel_inner_height_cm/(2*self.extrapolated_height_cm)))
        return enthalpy # J/kg
    def enthalpyincrease2T(self,x): #(kJ/kg to K)
        return self.inlet_temperature_K + x/(self.fuel_salt.heat_capacity_J_per_g_K)
    def T2enthalpyincrease(self,x): #(K to kJ/kg)
        return (x-self.inlet_temperature_K)*self.fuel_salt.heat_capacity_J_per_g_K
    def PlotAverageEnthalpyAndTemperature(self):
        z = np.linspace(-self.vessel_inner_height_cm/2,self.vessel_inner_height_cm/2,1000)
        enthalpy = self.AverageEnthalpy(z)
        plt.close('all')
        fig, ax = plt.subplots(dpi=150,constrained_layout=True)
        ax.plot(z,enthalpy*1E-3)
        ax.set_xlabel('z / cm')
        ax.set_ylabel('enthalpy increase  /  kJ kg$^{-1}$')
        secax = ax.secondary_yaxis('right', functions=(self.enthalpyincrease2T, self.T2enthalpyincrease))
        secax.set_ylabel('T / K')
    def PlotEnthalpyAndTemperatureInChannels(self):
        z = np.linspace(-self.vessel_inner_height_cm/2,self.vessel_inner_height_cm/2,1000)
        enthalpy_center = self.ChannelEnthalpy(0,z,center=True)
        enthalpy_1 = self.ChannelEnthalpy(4*2.54,z,center=False)
        enthalpy_2 = self.ChannelEnthalpy(self.vessel_inner_radius_cm-2.54,z,center=False)
        fig1,ax1 = plt.subplots(dpi=150)
        ax1.plot(z,enthalpy_center*1E-3,label='center')
        ax1.plot(z,enthalpy_1*1E-3,label='4 inches off-center')
        ax1.plot(z,enthalpy_2*1E-3,label='circumference')
        ax1.set_xlabel('z / cm')
        ax1.set_ylabel('enthalpy increase / kJ kg$^{-1}$')

        secax1 = ax1.secondary_yaxis('right', functions=(self.enthalpyincrease2T, self.T2enthalpyincrease))
        secax1.set_ylabel('T / K')
        ax1.plot([z[0],z[-1]],self.T2enthalpyincrease(np.array([450+273.15]*2)),label='melting point')
        ax1.plot([z[0],z[-1]],self.T2enthalpyincrease(np.array([730+273.15]*2)),label='max. operating temperature')
        leg1 = fig1.legend()
        leg1.set_draggable(True)
    def HaalandCorrelation(k,D,Re): # wall roughness k in mm, diameter D in mm
        one_over_sqrt_lambda = -1.8*np.log10((k/D/3.7)**1.11+6.9/Re)
        lambda_1 = 1/one_over_sqrt_lambda**2
        return lambda_1
    def CalculatePressureDropInOffcenterChannel(self):
        plt.close('all')
        fig1,ax1 = plt.subplots(dpi=150)
        G = self.fuel_salt.density_g_per_cm3*self.velocity_offcenter_channel_cm_per_s # g/(cm**2 s)      
        C_f = 16/self.reynolds_number_offcenter_channel # Fanning friction factor slide 130 in TH-design-equations-models_v0.pdf
        z = np.linspace(-self.vessel_inner_height_cm/2,self.vessel_inner_height_cm/2,1000)
        z_pH = z + self.vessel_inner_height_cm/2
        for ratio in [0.5,1,1.5]:
            delta_p_friction = -4*C_f*z_pH*G**2/(self.hydrolic_diameter_cm*2*self.fuel_salt.density_g_per_cm3)/10*1E-5 # bar 
            ax1.plot(z,delta_p_friction*ratio,label='friction @ {:.0f}% flow'.format(ratio*100))
        delta_p_gravity = -self.fuel_salt.density_g_per_cm3*981*z_pH/10*1E-5 # bar
        ax1.plot(z,delta_p_gravity,label='gravity')
        ax1.set_xlabel('z / cm')
        ax1.set_ylabel('delta_p / bar')
        ax1.legend()
        # lambda_1 = HaalandCorrelation(k,D,self.reynolds_number_center_channel)
    def GetLocalPressureDrop(self,Q): # Q in liters/s
        const = MSRE_salts.Constants()
        feet_fluid = const.ft_to_m*9.81*self.fuel_salt.density_g_per_cm3*1E3 # Pa
        weired_unit_of_alpha = feet_fluid/GPMtoLitersPerSecond(1)**2 # Pa s**2/l**2
        alpha = 10**(-5.178)*weired_unit_of_alpha # Pa s**2/l**2
        p = alpha*Q**2*1E-5 # bar
        return p
        
    def PlotTotalPressureDrop(self):
        Q = np.linspace(0,75.7*1.5,1000) # l/s
        p = self.GetLocalPressureDrop(Q)# bar
        plt.close('all')
        fig,ax = plt.subplots(dpi=150)
        ax.plot(Q,p)
        ax.set_xlabel('Q   (liters/s)')
        ax.set_ylabel('p / bar')
        

    
if __name__ == "__main__":
    core = Core()
    # core.PlotAverageEnthalpyAndTemperature()
    core.PlotEnthalpyAndTemperatureInChannels()
    print(core.reynolds_number_offcenter_channel)
    print(core.reynolds_number_center_channel)
    # core.CalculatePressureDropInOffcenterChannel()
    # core.PlotTotalPressureDrop()
    # print(core.GetMaximumPower(704-460, 4*2.54,center=False))