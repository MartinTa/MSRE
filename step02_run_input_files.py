#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:14:07 2021

@author: martin
"""

import os
from step01_generate_input_files import GetInputParameters


def GetRunCommandFromFileName(file_name):
    # return 'nohup /codes/SERPENT/sss2 -omp 1 {} > {}'.format(file_name,file_name + '.o')
    return f'nohup /codes/SERPENT/source/backup/serpent2/sss2 -omp 7 -noplot {file_name} > {file_name}.o'

def GetRunCommandFromFileNameWithoutPlotOrMC(file_name):
    # return 'nohup /codes/SERPENT/sss2 -omp 1 {} > {}'.format(file_name,file_name + '.o')
    return f'nohup /codes/SERPENT/source/backup/serpent2/sss2 -omp 1 -norun -noplot {file_name} > {file_name}.o'

def GetRunCommandFromTvec(T_vec):
    file_name = 'input_file_T0={:.2f}K_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K_T5={:.2f}K.in'.format(*T_vec)
    #file_path = os.path.join(folder_name,file_name)
    return GetRunCommandFromFileName(file_name)

if __name__ == '__main__':
    folder_name, T_matrix, rest = GetInputParameters()
    # T_matrix = [T_matrix[4]]
    run_commands = [GetRunCommandFromTvec(T_vec) for T_vec in T_matrix]
    full_run_command = ' && '.join(run_commands) + ' &' # && makes the commands go in sequence, each of which uses 5 threads, & makes them go in parallel
    print('running full run command now: ' + full_run_command)
    
    if not (os.path.basename(os.getcwd()) == folder_name):
        os.chdir(folder_name)
    os.system(full_run_command)