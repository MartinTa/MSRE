#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:35:04 2021

@author: martin
"""

import numpy as np
import os

# T1 / K ... nuclide temperature for doppler effect in all materials (fuel salt, graphite and steel). 
# T2 / K ... used for thermal expansion and density change of graphite
# T3 / K ... used for thermal expansion and density change of steel (hastalloy)
# T4 / K ... used for density change in fuel salt (excess gets automatically expelled from the core, decreasing the total fuel in the core when heated)
def GetInputStr(T1,T2,T3,T4):
    graphite_length_scale_factor = np.exp(5.52E-6*(T2-273.15)+0.001E-6/2*(T2-273.15)**2)
    steel_length_scale_factor = 1 + 15E-6*(T3-273.15-21)
    fuel_length_scale_factor = 1 + 78E-6*(T4-648.88-273.15) # reference density given at 1200 F
    
    graphite_density_scale_factor = 1/graphite_length_scale_factor**3
    steel_density_scale_factor = 1/steel_length_scale_factor**3
    fuel_density_scale_factor = 1/fuel_length_scale_factor**3
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
mat fuel {:.5f} tmp {:.5f} rgb 0 100 100""".format(-2.146*fuel_density_scale_factor,T1) + """
3007.09c -10.90
3006.09c -0.0005
9019.09c -66.80
4009.09c -6.27
40000.09c -10.92
92235.09c -1.67
92238.09c -3.44

% --- Moderator graphite :
% p. 87 msr operations ( robertson ) part i
% 1200 F, pg. 17 MSRE Design and Operations , part iii , nuclear analysis
mat moder {:.5f} tmp {:.5f} rgb 128 128 128 moder grmod 6000""".format(-1.86*graphite_density_scale_factor,T1) + """
5010.09c -1.592e-5
5011.09c -6.408e-5
23000.09c -0.0009
16000.09c -0.0005
6000.09c -99.99852
therm grmod {:.5f} grj2.18t grj2.20t""".format(T1) + """
% ignoring the oxygen b/c low content and XS

% hastelloy tank
mat tank {:.5f} tmp {:.5f} rgb 120 120 230""".format(-8.86*steel_density_scale_factor,T1) + """
14030.09c -0.00030872
74186.09c -0.0014215
25055.09c -0.008
74184.09c -0.001532
74183.09c -0.0007155
74182.09c -0.001325
28058.09c -0.4721201092
42092.09c -0.023744
26058.09c -0.000141
42094.09c -0.0148
42095.09c -0.025472
42096.09c -0.026688
42097.09c -0.01528
42098.09c -0.038608
26056.09c -0.045877
26057.09c -0.0010595
26054.09c -0.0029225
42100.09c -0.015408
14028.09c -0.00922297
14029.09c -0.00046832
24050.09c -0.0030415
24052.09c -0.0586523
24053.09c -0.0066507
24054.09c -0.0016555
29065.09c -0.00107905
29063.09c -0.00242095
28064.09c -0.0064191286
28061.09c -0.0079053205
28060.09c -0.1818598208
28062.09c -0.025205621

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
surf 2993 sph 0.0 0.0 0 {:.5f} % dummy outer surface """.format(220*steel_length_scale_factor) + """
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
surf 1231 cyl {:.5f} {:.5f} 2.413 %1/20 inconel , approximate as hastelloy""".format(*list(np.array([5.08, 5.08])*graphite_length_scale_factor)) + """
surf 1232 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([-5.08, 5.08])*graphite_length_scale_factor)) + """
surf 1233 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([-5.08, -5.08])*graphite_length_scale_factor)) + """
surf 1234 cyl {:.5f} {:.5f} 2.413""".format(*list(np.array([5.08, -5.08])*graphite_length_scale_factor)) + """
surf 1235 cyl {:.5f} {:.5f} 2.54 %1/20 inconel , approximate as hastelloy""".format(*list(np.array([5.08,5.08])*graphite_length_scale_factor)) + """
surf 1236 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([-5.08, 5.08])*graphite_length_scale_factor)) + """
surf 1237 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([-5.08, -5.08])*graphite_length_scale_factor)) + """
surf 1238 cyl {:.5f} {:.5f} 2.54""".format(*list(np.array([5.08, -5.08])*graphite_length_scale_factor)) + """

% top of control rods
surf 9000 pz 81.28 %150.876

% CR surfaces
surf cr11 cyl 0 0 1.0033
surf cr12 cyl 0 0 1.0668
surf cr13 cyl 0 0 1.3716
surf cr14 cyl 0 0 1.4478

% --- Cells :
cell 300 0 fill 300 -3000 3003 -3004 2000 2001 2002 2003 % central mod
cell 401 0 fill 2 -2996 3002 -2995 2000 2001 2002 2003 % upper plenum
cell 402 0 fill 2 -2996 -3001 -2995 % lower plenum
cell 404 0 fill 2 3004 -3002 -3000 % between graphite and upper plenum
cell 405 0 fill 2 3001 -3003 -3000 % between graphite and lower plenum

% CR cells
cell cr21 CR1 fill 6 -cr11 -9000 3001
cell cr31 CR2 fill 6 -cr11 -9000 3001
cell cr41 CR3 fill 6 -cr11 -9000 3001
cell cr22 CR1 fill 4 cr11 -cr12 -9000 3001
cell cr32 CR2 fill 4 cr11 -cr12 -9000 3001
cell cr42 CR3 fill 4 cr11 -cr12 -9000 3001
cell cr23 CR1 fill 5 cr12 -cr13 -9000 3001
cell cr33 CR2 fill 5 cr12 -cr13 -9000 3001
cell cr43 CR3 fill 5 cr12 -cr13 -9000 3001
cell cr24 CR1 fill 4 cr13 -cr14 -9000 3001
cell cr34 CR2 fill 4 cr13 -cr14 -9000 3001
cell cr44 CR3 fill 4 cr13 -cr14 -9000 3001
cell cr25 CR1 fill 6 cr14 -9000 3001
cell cr35 CR2 fill 6 cr14 -9000 3001
cell cr45 CR3 fill 6 cr14 -9000 3001
cell cr26 CR1 fill 6 9000
cell cr36 CR2 fill 6 9000
cell cr46 CR3 fill 6 9000
cell cr27 CR1 fill 6 -3001
cell cr37 CR2 fill 6 -3001
cell cr47 CR3 fill 6 -3001

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
cell 710 0 fill 3 -1234 %-5000 5001
cell 711 0 tank 1234 -1238 %-5000 5001
cell 712 0 fill 2 1238 -2003 %-5000 5001

% CR 1 guide tube
cell 1999 0 fill CR1 -1231 %-5000 5001
cell 1998 0 fill 4 1231 -1235 %-5000 5001
cell 1997 0 fill 2 1235 -2000 %-5000 5001


% CR 2 guide tube
cell 1996 0 fill CR2 -1232 %-5000 5001
cell 1995 0 fill 4 1232 -1236 %-5000 5001
cell 1994 0 fill 2 1236 -2001 %-5000 5001


% CR 3 guide tube
cell 1993 0 fill CR3 -1233 %-5000 5001
cell 1992 0 fill 4 1233 -1237 %-5000 5001
cell 1991 0 fill 2 1237 -2002 %-5000 5001

% rest of the vessel + outside
cell 299 0 fill 2 3000 -2999 3001 -3002 % fuel around mod , between downcomer
cell 298 0 fill 4 2999 -2998 3001 -3002 % downcomer wall
cell 297 0 fill 2 2998 -2997 3001 -3002 % downcomer
cell 296 0 fill 4 2997 -2996 3001 -3002 % reactor vessel
cell 295 0 fill 4 2995 -2994 3002 % upper vessel lid7
cell 29 0 fill 4 2995 -2994 -3001 % upper vessel lid
cell 403 0 outside 2994 -2993
cell 301 0 outside 2996 -2994
cell 999 0 outside 2993
%cell 600 0 outside 2994

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
set pop 5000 500 50 %50000 600 100

% --- Geometry and mesh plots :
plot 1 1500 1500
plot 2 1500 1500
plot 3 1500 1500
mesh 1 1500 1500
mesh 2 1500 1500
mesh 3 1500 1500

% neutron spectrum measurement
ene eGrid 4 scale238
det spectralFuel dr 0 fuel de eGrid
det spectralMod dr 0 moder de eGrid

% graphite is just at one temperature for this
% therm grmod 922 grj2.18t grj2.20t
trans u TR1 5.08 5.08 208.0
trans u TR2 5.08 5.08 161.9055
trans u TR3 5.08 5.08 115.811
trans u TR4 5.08 5.08 69.7165
trans u TR5 5.08 5.08 23.622

% ---- BRANCHES ------------
branch fuel0 stp fuel -2.2818562220275704 633.0
branch fuel1 stp fuel -2.2496135461743254 700.0
branch fuel2 stp fuel -2.2023356233843003 800.0
branch fuel3 stp fuel -2.1560512943549197 900.0
branch fuel4 stp fuel -2.1107396777000536 1000.0
branch fuel5 stp fuel -2.066380330877196 1100.0
branch fuel6 stp fuel -2.022953240964719 1200.0
branch fuel7 stp fuel -1.9804388156329515 1300.0
branch fuel8 stp fuel -1.9388178743050104 1400.0
branch fuel9 stp fuel -1.8980716395033954 1500.0
branch fuel10 stp fuel -1.8581817283784454 1600.0
branch fuel11 stp fuel -1.819130144414831 1700.0
branch fuel12 stp fuel -1.7808992693123449 1800.0
branch fuel13 stp fuel -1.7434718550373258 1900.0
branch fuel14 stp fuel -1.7068310160411293 2000.0
branch rod0 tra CR1 TR1
branch rod1 tra CR1 TR2
branch rod2 tra CR1 TR3
branch rod3 tra CR1 TR4
branch rod4 tra CR1 TR5

%coef 1
%0
%15 fuel0 fuel1 fuel2 fuel3 fuel4 fuel5 fuel6 fuel7 fuel8 fuel9 fuel10 fuel11 fuel12 fuel13 fuel14
%5 rod0 rod1 rod2 rod3 rod4

% --- Detector for tallying the flux energy spectrum
%     The energy grid used for tallying will be defined later

det EnergyDetector de MyEnergyGrid

% --- Define the energy grid to be used with the detector
%     Grid type 3 (bins have uniform lethargy width)
%     500 bins between 1e-11 MeV and 2e1 MeV.

ene MyEnergyGrid 3 500 1e-11 2e1

set bc 1
"""
    return input_file_str

def RunSerpent(file_name):
    os.system('nohup /codes/SERPENT/sss2 -opm 3 {} > {} &'.format(file_name,file_name+'.o'))


if __name__ == "__main__":
    T1 = 922       # K # 273.15 #
    T2 = T1 # 273.15    # K
    T3 = T1 # 273.15+21 # K
    T4 = T1 # 273.15    # K
    input_file_str = GetInputStr(T1,T2,T3,T4)
    file_name = 'input_file_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K'.format(T1,T2,T3,T4)
    with open(file_name,'w') as f:
        f.write(input_file_str)
    # RunSerpent(file_name)
    