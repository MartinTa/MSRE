#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:14:07 2021

@author: martin
"""

import src.input_file as input_file

def GetInputParameters():
    folder_name = 'data_4'
    T_low = 850   # lower temperature
    T_cen = 900   # center temperature
    T_hig = 950  # higher temperature
                 
    T_matrix_global  = [
        [800]*6,
        [825]*6,
        [T_low]*6,
        [875]*6,
        [T_cen]*6,
        [925]*6,
        [T_hig]*6,
        [975]*6,
        [1000]*6]
    T_matrix_high = [
        [T_hig,T_cen,T_cen,T_cen,T_cen,T_cen],
        [T_cen,T_hig,T_cen,T_cen,T_cen,T_cen],
        [T_cen,T_cen,T_hig,T_cen,T_cen,T_cen],
        [T_cen,T_cen,T_cen,T_hig,T_cen,T_cen],
        [T_cen,T_cen,T_cen,T_cen,T_hig,T_cen],
        [T_cen,T_cen,T_cen,T_cen,T_cen,T_hig]]
    T_matrix_low = [
        [T_low,T_cen,T_cen,T_cen,T_cen,T_cen],
        [T_cen,T_low,T_cen,T_cen,T_cen,T_cen],
        [T_cen,T_cen,T_low,T_cen,T_cen,T_cen],
        [T_cen,T_cen,T_cen,T_low,T_cen,T_cen],
        [T_cen,T_cen,T_cen,T_cen,T_low,T_cen],
        [T_cen,T_cen,T_cen,T_cen,T_cen,T_low]]
    T_matrix = T_matrix_global + T_matrix_high + T_matrix_low
    return folder_name, T_matrix, (T_matrix_global, T_matrix_high, T_matrix_low)

if __name__ == "__main__":
    folder_name, T_matrix, rest = GetInputParameters()
    # T_matrix = [T_matrix[4]]
    for T_vec in T_matrix:
        input_file.GenerateFile(*T_vec,folder_name)