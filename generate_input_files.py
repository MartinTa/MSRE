#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:06:51 2021

@author: martin
"""

import input_file

T_low = 850   # lower temperature
T_cen = 900   # center temperature
T_hig = 950  # higher temperature

T_matrix = [[T_cen,T_cen,T_cen,T_cen,T_cen],
            [T_hig,T_hig,T_hig,T_hig,T_hig],
            [T_low,T_low,T_low,T_low,T_low],
            [T_hig,T_cen,T_cen,T_cen,T_cen],
            [T_cen,T_hig,T_cen,T_cen,T_cen],
            [T_cen,T_cen,T_hig,T_cen,T_cen],
            [T_cen,T_cen,T_cen,T_hig,T_cen],
            [T_cen,T_cen,T_cen,T_cen,T_hig],
            [T_low,T_cen,T_cen,T_cen,T_cen],
            [T_cen,T_low,T_cen,T_cen,T_cen],
            [T_cen,T_cen,T_low,T_cen,T_cen],
            [T_cen,T_cen,T_cen,T_low,T_cen],
            [T_cen,T_cen,T_cen,T_cen,T_low]]

T_matrix2 = [[800]*5,
             [825]*5,
             [875]*5,
             [925]*5,
             [975]*5,
             [1000]*5,
             [1025]*5,
             [1050]*5]

T_matrix3 = [[900,900,900,900,900],
             [901,900,900,900,900],
             [950,900,900,900,900]]

for T_vec in T_matrix2:
    input_file.GenerateFile(*T_vec,folder_name = 'serpent_data_7')