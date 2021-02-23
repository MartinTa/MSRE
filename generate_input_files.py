#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:06:51 2021

@author: martin
"""

import input_file

T_low = 800   # lower temperature
T_cen = 900   # center temperature
T_hig = 1000  # higher temperature

T_matrix = [[T_cen,T_cen,T_cen,T_cen,T_cen],
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

for T_vec in T_matrix:
    input_file.GenerateFile(*T_vec)