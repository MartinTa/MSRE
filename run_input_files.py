#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:20:42 2021

@author: martin
"""
import os

def GetRunCommandFromFileName(file_name):
    return 'nohup /codes/SERPENT/sss2 -omp 5 {} > {}'.format(file_name,file_name + '.o')

def GetRunCommandFromTvec(T_vec):
    file_name = 'input_file_T0={:.2f}K_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K.in'.format(*T_vec)
    folder_name = 'serpent_data'
    file_path = os.path.join(folder_name,file_name)
    return GetRunCommandFromFileName(file_path)

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

run_commands = [GetRunCommandFromTvec(T_vec) for T_vec in T_matrix]
full_run_command = ' && '.join(run_commands) + ' &' # && makes the commands go in sequence, each of which uses 5 threads
print('running full run command now: ' + full_run_command)
os.system(full_run_command)
