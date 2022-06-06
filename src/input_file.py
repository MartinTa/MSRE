#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:35:04 2021

@author: martin
"""

import numpy as np
import os

def GetTemperatureMarker(T): # produces from e.g. T = 599 the string 03 and from T = 600 the string 06
    return '{:02d}'.format((T//300)*3)

# T0 / K ... nuclide temperature for doppler effect in fuel salt
# T1 / K ... nuclide temperature for doppler effect in all other materials
# T2 / K ... used for thermal expansion and density change of graphite
# T3 / K ... used for thermal expansion and density change of steel (hastalloy)
# T4 / K ... used for density change in fuel salt (excess gets automatically expelled from the core, decreasing the total fuel in the core when heated)
# T5 / K ... thermal crosssection library for graphite
def GetInputStr(T0,T1,T2,T3,T4,T5):
    graphite_length_scale_factor = np.exp(5.52E-6*(T2-273.15)+0.001E-6/2*(T2-273.15)**2)
    steel_length_scale_factor = 1 + 15E-6*(T3-273.15-21)
    fuel_length_scale_factor = 1 + 78E-6*(T4-648.88-273.15) # reference density given at 1200 F
    enrichment = 0.33 # 0.29 gives criticality
    
    graphite_density_scale_factor = 1/graphite_length_scale_factor**3
    steel_density_scale_factor = 1/steel_length_scale_factor**3
    fuel_density_scale_factor = 1/fuel_length_scale_factor**3
    #print(f'fuel density scale factor = {fuel_density_scale_factor:.8f}')
    
    T0_marker = GetTemperatureMarker(T0)
    T1_marker = GetTemperatureMarker(T1)
    input_file_str = """% --- MSR cluster ------------------------------------------
set title "MSR2G - partially - enriched -U-full - core "

%% --- get the stringer unit cell (graphite rod)
surf 11 inf
surf 12 inf
surf 13 inf
surf 14 inf
surf 15 inf
cell 111 2 fuel -11
cell 112 3 moder -12
cell 113 4 tank -13
cell 114 5 ctrlPois -14
cell 115 6 air -15

% --- Single unit cell
% 4 bounding planes of stringer
surf 1 px {:.5f}""".format(-2.54*graphite_length_scale_factor) + """
surf 2 px {:.5f}""".format(2.54*graphite_length_scale_factor) + """
surf 3 py {:.5f}""".format(-2.54*graphite_length_scale_factor) + """
surf 4 py {:.5f}""".format(2.54*graphite_length_scale_factor) + """

% 4 square prisms form slot edges
surf 5 sqc {:.5f} {:.5f} {:.5f} {:.5f}""".format(*list(np.array([3.556, 0, 1.524, 0.508 ])*graphite_length_scale_factor)) + """
surf 6 sqc {:.5f} {:.5f} {:.5f} {:.5f}""".format(*list(np.array([-3.556, 0, 1.524, 0.508])*graphite_length_scale_factor)) + """
surf 7 sqc {:.5f} {:.5f} {:.5f} {:.5f}""".format(*list(np.array([0, 3.556, 1.524, 0.508 ])*graphite_length_scale_factor)) + """
surf 8 sqc {:.5f} {:.5f} {:.5f} {:.5f}""".format(*list(np.array([0, -3.556, 1.524, 0.508])*graphite_length_scale_factor)) + """
cell 11 1 fill 3 1 -2 3 -4 5 6 7 8
cell 12 1 fill 2 -1 6 -4 3% behind in x
cell 13 1 fill 2 2 5 -4 3% in front in x
cell 14 1 fill 2 -3 8 % behind in y
cell 15 1 fill 2 4 7 % front of y
cell 16 1 fill 2 -5 % salt in +x channel
cell 17 1 fill 2 -6
cell 18 1 fill 2 -7
cell 19 1 fill 2 -8
cell 20 1 outside -1 -2 3
cell 21 1 outside 2 -2 3
cell 22 1 outside 4
cell 23 1 outside -3

%% --- problem materials
% --- Fuel ( Partially enriched uranium ):
% 1200 F, pg. 17 MSRE Design and Operations , part iii , nuclear analysis
mat fuel {:.5f} tmp {:.5f} rgb 0 100 100""".format(-2.146*fuel_density_scale_factor,T0) + """
3007.{}c -10.90""".format(T0_marker) + """
3006.{}c -0.0005""".format(T0_marker) + """
9019.{}c -66.80""".format(T0_marker) + """
4009.{}c -6.27""".format(T0_marker) + """
40000.{}c -10.92""".format(T0_marker) + """
92235.{}c {:.2f}""".format(T0_marker,-5.11*enrichment) + """
92238.{}c {:.2f}""".format(T0_marker,-5.11*(1-enrichment)) + """

% --- Moderator graphite :
% p. 87 msr operations ( robertson ) part i
% 1200 F, pg. 17 MSRE Design and Operations , part iii , nuclear analysis
mat moder {:.5f} tmp {:.5f} rgb 128 128 128 moder grmod 6000""".format(-1.86*graphite_density_scale_factor,T1) + """
5010.{}c -1.592e-5""".format(T1_marker) + """
5011.{}c -6.408e-5""".format(T1_marker) + """
23000.{}c -0.0009""".format(T1_marker) + """
16000.{}c -0.0005""".format(T1_marker) + """
6000.{}c -99.99852""".format(T1_marker) + """
therm grmod {:.5f} grj2.18t grj2.20t""".format(T5) + """
% ignoring the oxygen b/c low content and XS

% hastelloy tank
mat tank {:.5f} tmp {:.5f} rgb 120 120 230""".format(-8.86*steel_density_scale_factor,T1) + """
14030.{}c -0.00030872""".format(T1_marker) + """
74186.{}c -0.0014215""".format(T1_marker) + """
25055.{}c -0.008""".format(T1_marker) + """
74184.{}c -0.001532""".format(T1_marker) + """
74183.{}c -0.0007155""".format(T1_marker) + """
74182.{}c -0.001325""".format(T1_marker) + """
28058.{}c -0.4721201092""".format(T1_marker) + """
42092.{}c -0.023744""".format(T1_marker) + """
26058.{}c -0.000141""".format(T1_marker) + """
42094.{}c -0.0148""".format(T1_marker) + """
42095.{}c -0.025472""".format(T1_marker) + """
42096.{}c -0.026688""".format(T1_marker) + """
42097.{}c -0.01528""".format(T1_marker) + """
42098.{}c -0.038608""".format(T1_marker) + """
26056.{}c -0.045877""".format(T1_marker) + """
26057.{}c -0.0010595""".format(T1_marker) + """
26054.{}c -0.0029225""".format(T1_marker) + """
42100.{}c -0.015408""".format(T1_marker) + """
14028.{}c -0.00922297""".format(T1_marker) + """
14029.{}c -0.00046832""".format(T1_marker) + """
24050.{}c -0.0030415""".format(T1_marker) + """
24052.{}c -0.0586523""".format(T1_marker) + """
24053.{}c -0.0066507""".format(T1_marker) + """
24054.{}c -0.0016555""".format(T1_marker) + """
29065.{}c -0.00107905""".format(T1_marker) + """
29063.{}c -0.00242095""".format(T1_marker) + """
28064.{}c -0.0064191286""".format(T1_marker) + """
28061.{}c -0.0079053205""".format(T1_marker) + """
28060.{}c -0.1818598208""".format(T1_marker) + """
28062.{}c -0.025205621""".format(T1_marker) + """

% control rod absorber material
% operations report i; p. 102
% 70 wtpct gad III oxide , 30 wtpct al III oxide
mat ctrlPois -5.873 rgb 5 40 96
64000.09c 0.003862068965517241
13027.09c 0.005884660651235779
8016.09c 0.014620094425129529

mat air -0.001225 rgb 230 230 255
8016.09c 0.21
7014.09c 0.79

% % --- Lattice
lat 300 1 {:.5f} {:.5f} 30 30 {:.5f}""".format(*list(np.array([2.54, 2.54, 5.08])*graphite_length_scale_factor)) + """
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

% --- Surfaces :
surf 3000 cyl 0.0 0.0 {:.5f} % p. 78""".format(70.1675*graphite_length_scale_factor) + """
surf 2999 cyl 0.0 0.0 {:.5f} % central mod -> core container : fuel""".format(70.485*steel_length_scale_factor) + """
surf 2998 cyl 0.0 0.0 {:.5f} % core container ID -> OD : hastelloy""".format(71.12*steel_length_scale_factor) + """
surf 2997 cyl 0.0 0.0 {:.5f} % vessel ID""".format(73.66*steel_length_scale_factor) + """
surf 2996 cyl 0.0 0.0 {:.5f} % vessel OD""".format(75.08875*steel_length_scale_factor) + """
surf 2995 sph 0.0 0.0 0 {:.5f} % vessel lid ID, rough geometry""".format(109.6915*steel_length_scale_factor) + """
surf 2994 sph 0.0 0.0 0 {:.5f} % vessel lid OD, rough geometry""".format(110.6560*steel_length_scale_factor) + """
%surf 2993 sph 0.0 0.0 0 {:.5f} % dummy outer surface """.format(220*steel_length_scale_factor) + """
surf 3001 pz {:.5f}""".format(-81.28*steel_length_scale_factor) + """
surf 3002 pz {:.5f}""".format(81.28*steel_length_scale_factor) + """
surf 3003 pz {:.5f}""".format(-80.645*graphite_length_scale_factor) + """
surf 3004 pz {:.5f}""".format(80.645*graphite_length_scale_factor) + """

% 198.12 was given here previously for surf 3002 and using 0 for 3001, which is 78 inches and the effective core height as given in table 5.4, MSRE Design and Operation I

% control rod slots :
surf 2000 cyl  {:.5f} {:.5f} {:.5f}""".format(*list(np.array([5.08, 5.08, 3])*graphite_length_scale_factor)) + """
surf 2001 cyl  {:.5f} {:.5f} {:.5f}""".format(*list(np.array([-5.08, 5.08, 3])*graphite_length_scale_factor)) + """
surf 2002 cyl  {:.5f} {:.5f} {:.5f}""".format(*list(np.array([-5.08, -5.08, 3])*graphite_length_scale_factor)) + """

% experiment slot
surf 2003 cyl {:.5f} {:.5f} {:.5f}""".format(*list(np.array([5.08, -5.08, 3])*graphite_length_scale_factor)) + """

% CR / experiment tubes
surf 1231 cyl {:.5f} {:.5f} 2.413 %1/20 inconel , approximate as hastelloy""".format(*list(np.array([5.08, 5.08])*steel_length_scale_factor)) + """
surf 1232 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([-5.08, 5.08])*steel_length_scale_factor)) + """
surf 1233 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([-5.08, -5.08])*steel_length_scale_factor)) + """
surf 1234 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([5.08, -5.08])*steel_length_scale_factor)) + """
surf 1235 cyl {:.5f} {:.5f} 2.54 %1/20 inconel , approximate as hastelloy""".format(*list(np.array([5.08,5.08])*steel_length_scale_factor)) + """
surf 1236 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([-5.08, 5.08])*steel_length_scale_factor)) + """
surf 1237 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([-5.08, -5.08])*steel_length_scale_factor)) + """
surf 1238 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([5.08, -5.08])*steel_length_scale_factor)) + """

% top of control rods
%surf 9000 pz 81.28 %150.876

% CR surfaces
surf cr11 cyl 0 0 1.0033
surf cr12 cyl 0 0 1.0668
surf cr13 cyl 0 0 1.3716
surf cr14 cyl 0 0 1.4478

% --- Cells :
cell 300 0 fill 300 -3000 3003 -3004 2000 2001 2002 2003 % central mod
cell 401 0 fill 2 -2996 3002 -2995 2000 2001 2002 2003 % upper plenum
cell 402 0 fill 2 -2996 -3001 -2995 2000 2001 2002 2003% lower plenum
cell 404 0 fill 2 3004 -3002 -3000 2000 2001 2002 2003%1235 1236 1237 1238% between graphite and upper plenum
cell 405 0 fill 2 3001 -3003 -3000 2000 2001 2002 2003%1235 1236 1237 1238% between graphite and lower plenum

% CR cells
cell cr21 CR1 fill 6 -cr11 -3004 3003 % 3004 is upper graphite plane, 3003 is lower graphite plane
cell cr31 CR2 fill 6 -cr11 -3004 3003
cell cr41 CR3 fill 6 -cr11 -3004 3003
cell cr22 CR1 fill 4 cr11 -cr12 -3004 3003 % steel
cell cr32 CR2 fill 4 cr11 -cr12 -3004 3003
cell cr42 CR3 fill 4 cr11 -cr12 -3004 3003
cell cr23 CR1 fill 5 cr12 -cr13 -3004 3003 % CR poison
cell cr33 CR2 fill 5 cr12 -cr13 -3004 3003
cell cr43 CR3 fill 5 cr12 -cr13 -3004 3003
cell cr24 CR1 fill 4 cr13 -cr14 -3004 3003
cell cr34 CR2 fill 4 cr13 -cr14 -3004 3003
cell cr44 CR3 fill 4 cr13 -cr14 -3004 3003
cell cr25 CR1 fill 6 cr14 -3004 3003
cell cr35 CR2 fill 6 cr14 -3004 3003
cell cr45 CR3 fill 6 cr14 -3004 3003
cell cr26 CR1 fill 6 3004
cell cr36 CR2 fill 6 3004
cell cr46 CR3 fill 6 3004
cell cr27 CR1 fill 6 -3003
cell cr37 CR2 fill 6 -3003
cell cr47 CR3 fill 6 -3003

% CONTROL ROD POSITIONS
% ordered like quadrants are
% 0 corresponds to bottom of moderator , but the poison is only
% 59.4 " long (p. 107 , msre ops i). ie 150.876 cm
% so , the dropped rod for max worth is z- translated up 23.622 cm
% for a pulled rod , just move it out of the core . z =208.0 works well
trans CR1 5.08 5.08 208.0
trans CR2 -5.08 5.08 208.0
trans CR3 -5.08 -5.08 208.0

% approximate the experiment tube as a tube full of graphite
cell 710 0 fill 3 -1234 -2995%-5000 5001
cell 711 0 tank 1234 -1238 -2995%-5000 5001
cell 712 0 fill 2 1238 -2003 -2995%-5000 5001

% CR 1 guide tube
cell 1999 0 fill CR1 -1231 -2995%-5000 5001
cell 1998 0 fill 4 1231 -1235 -2995%-5000 5001
cell 1997 0 fill 2 1235 -2000 -2995%-5000 5001


% CR 2 guide tube
cell 1996 0 fill CR2 -1232 -2995%-5000 5001
cell 1995 0 fill 4 1232 -1236 -2995%-5000 5001
cell 1994 0 fill 2 1236 -2001 -2995%-5000 5001


% CR 3 guide tube
cell 1993 0 fill CR3 -1233 -2995%-5000 5001
cell 1992 0 fill 4 1233 -1237 -2995%-5000 5001
cell 1991 0 fill 2 1237 -2002 -2995%-5000 5001

% rest of the vessel + outside
cell 299 0 fill 2 3000 -2999 3001 -3002 % fuel around mod , between downcomer
cell 298 0 fill 4 2999 -2998 3001 -3002 % downcomer wall
cell 297 0 fill 2 2998 -2997 3001 -3002 % downcomer
cell 296 0 fill 4 2997 -2996 3001 -3002 % reactor vessel
cell 295 0 fill 4 2995 -2994 3002 % upper vessel lid7
cell 29 0 fill 4 2995 -2994 -3001 % upper vessel lid

%cell 403 0 outside 2994 : 2996 % outside sphere and outside cylinder (union operator :)
cell 403 0 outside 2994 %-2993
cell 301 0 outside 2996 -2994
%cell 999 0 outside 2993

% --- Cross section data library file path :
set acelib "/codes/SERPENT/xsdata/endfb7.xsdata" %"endfb7u.xsdata"
set nfylib "/codes/SERPENT/xsdata/sss_endfb7.nfy" %"sss_endfb7.nfy"2994
set declib "/codes/SERPENT/xsdata/sss_endfb7.dec" %"sss_endfb7.dec"

% --- group constant generation :
set gcu 2 3

% --- group structure
% option 1
set nfg 4 7.3000e-7 2.9023e-5 9.1188e-3

% option 2
% set nfg 4 1.8554e-6 2.9023e-5 9.1188e-3

% --- Neutron population and criticality cycles :
set pop 10000 5000 200 %50000 600 100

% --- Geometry and mesh plots :
plot 1 1500 1500
plot 2 1500 1500
plot 3 1500 1500
plot 2 1500 1500 5.08
plot 2 1500 1500 -5.08
plot 3 1500 1500 0 -20 20 -20 20
mesh 1 1500 1500
mesh 2 1500 1500
mesh 3 1500 1500

% neutron spectrum measurement
ene eGrid 4 scale238
det spectralFuel dr 0 fuel de eGrid
det spectralMod dr 0 moder de eGrid

% graphite is just at one temperature for this
% therm grmod 922 grj2.18t grj2.20t
% trans u TR1 5.08 5.08 208.0
% trans u TR2 5.08 5.08 161.9055
% trans u TR3 5.08 5.08 115.811
% trans u TR4 5.08 5.08 69.7165
% trans u TR5 5.08 5.08 23.622

% --- Detector for tallying the flux energy spectrum

det EnergyDetector de MyEnergyGrid

% --- Define the energy grid to be used with the detector
%     Grid type 3 (bins have uniform lethargy width)
%     500 bins between 1e-11 MeV and 2e1 MeV.

ene MyEnergyGrid 3 500 1e-11 2e1

set bc 1
set his 1

"""
    return input_file_str

def RunSerpent(file_name): # currently not useful since this script can not be run on server since numpy is not yet installed there
    os.system('nohup /codes/SERPENT/sss2 -omp 2 {} > {} &'.format(file_name,file_name+'.o'))

def GenerateFile(T0,T1,T2,T3,T4,T5,folder_name):
    input_file_str = GetInputStr(T0,T1,T2,T3,T4,T5)
    file_path = os.path.join(folder_name,'input_file_T0={:.2f}K_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K_T5={:.2f}K.in'.format(T0,T1,T2,T3,T4,T5))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(file_path,'w') as f:
        f.write(input_file_str)
    # RunSerpent(file_name)

if __name__ == "__main__":
    T0 = 900
    T1 = 900   # K
    T2 = T1    # K
    T3 = T1    # K
    T4 = T1    # K
    GenerateFile(T0,T1,T2,T3,T4,folder_name = 'temp')
    # GenerateFile(T0,T1,T2,T3,950,folder_name = 'temp')