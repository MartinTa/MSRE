#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:28:06 2021

@author: martin
"""

import MSRE_salts
import scipy.special
import numpy as np

fuel_salt = MSRE_salts.fuel_salt
coolant_salt = MSRE_salts.coolant_salt

def InchesToCm(x):
    return x*2.54

def psigToMPa(x): # psig is relative to ambient pressure of 14.7 psia (absolute)
    return (x+14.7)*6.894757E-3

class CoreParameters():
    def __init__(self):
        self.graphite_radius_inches = 55.25# MSRE Design and Operation I, Table 5.2
        self.graphite_height_inches = 63.5 # Fig. 5.6
        self.maximum_He_pressure_in_pump_bowl_psig = 25 # # MSRE Design and Operation VI REV3
        self.vessel_inner_radius_inches = 58 # MSRE Design and Operation I, Table 5.2
        self.vessel_inner_height_inches = 68
        self.extrapolated_radius_inches = 29.5 # MSRE Design and Operation I, Table 5.4 
        self.extrapolated_height_inches = 78 # -||-  
        
        self.graphite_radius_cm = InchesToCm((self.graphite_radius_inches))
        self.graphite_height_cm = InchesToCm((self.graphite_height_inches))
        self.maximum_He_pressure_in_pump_bowl_MPa = psigToMPa(self.maximum_He_pressure_in_pump_bowl_psig)
        self.vessel_inner_radius_cm = InchesToCm(self.vessel_inner_radius_inches)
        self.vessel_inner_height_cm = InchesToCm(self.vessel_inner_height_inches)
        self.extrapolated_radius_cm = InchesToCm(self.extrapolated_radius_inches)
        self.extrapolated_height_cm = InchesToCm(self.extrapolated_height_inches)
        
        self.thermal_power_MW = 8.00 #
        self.PrintMetricParameters()        
    def PrintMetricParameters(self):
        print('graphite_radius = {:.2f} cm'.format(self.graphite_radius_cm))
        print('graphite_height = {:.2f} cm'.format(self.graphite_height_cm))
        print('maximum_He_pressure_in_pump_bowl = {:.4f} MPa'.format(self.maximum_He_pressure_in_pump_bowl_MPa))
        print('vessel_inner_radius = {:.2f} cm'.format(self.vessel_inner_radius_cm))
        print('extrapolated_radius = {:.2f} cm'.format(self.extrapolated_radius_cm))
        print('extrapolated_height = {:.2f} cm'.format(self.extrapolated_height_cm))
        
    def PowerDensity(self,r,z):
        V = self.extrapolated_radius_cm**2*np.pi*self.extrapolated_height_cm # cm**3
        q_0_pp = 3.63817*self.thermal_power_MW/V # MW/cm**3
        return q_0_pp*scipy.special.j0(2.40482555769*r/self.extrapolated_radius_cm)*np.cos(np.pi*z/self.extrapolated_height_cm)
    
core_parameters = CoreParameters()
# Pressure drop: Fig. 5.10 in MSRE Design and Operation I, Table 5.2
