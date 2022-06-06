#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:09:09 2021

@author: martin
"""

import serpentTools
import os
import numpy as np
import matplotlib.pyplot as plt
from step01_generate_input_files import GetInputParameters

def GetKandRhofromTMatrix(T_matrix,folder_name):
    k_eff = np.zeros(len(T_matrix))
    k_eff_std = np.zeros_like(k_eff)
    rho = np.zeros_like(k_eff_std)
    rho_std = np.zeros_like(k_eff_std)
    for n,T_vec in enumerate(T_matrix):
        file_name = 'input_file_T0={:.2f}K_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K_T5={:.2f}K.in_res.m'.format(*T_vec)
        file_path = os.path.join(folder_name,file_name)
        data = serpentTools.read(file_path)
        resdata = data.resdata
        k_eff[n] = resdata['impKeff'][0]
        k_eff_std[n] = resdata['impKeff'][1]
        rho[n] = (k_eff[n]-1)/k_eff[n]
        rho_std[n] = k_eff_std[n]/k_eff[n]**2
    return k_eff, k_eff_std, rho, rho_std  
    
def EvaluateResults(): # Using the definition: alpha = 1/k dk/dT = d/dT ln(k)
    labels = ['Doppler fuel', 'Doppler rest', 'thermal expansion graphite', 'thermal expansion steel', 'density salt', 'thermal scattering graphite']
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors_1 = [colors[1],colors[6],colors[4],colors[5],colors[3],colors[2],colors[7]]
    folder_name, T_matrix, (T_matrix_global, T_matrix_high, T_matrix_low) = GetInputParameters()
    k_eff, k_eff_std, rho, rho_std = GetKandRhofromTMatrix(T_matrix_global,folder_name)
    T_vec = [T[0] for T in T_matrix_global]
    plt.close('all')
    plt.errorbar(T_vec,rho*1E5,rho_std*1E5,fmt='o-',capsize=5,label='$T_{all}$')
    plt.ylabel(r'$\rho$ / pcm')
    plt.xlabel('T / K')
    plt.grid()
    index_900 = T_vec.index(900)
    index_950 = T_vec.index(950)
    index_850 = T_vec.index(850)
    
    k_eff_high, k_eff_std_high, rho_high, rho_std_high = GetKandRhofromTMatrix(T_matrix_high,folder_name)
    k_eff_low, k_eff_std_low, rho_low, rho_std_low = GetKandRhofromTMatrix(T_matrix_low,folder_name)
    
    # individual and sum of individual 1/k dk/dT
    alpha_high = np.zeros(len(T_matrix_high))               # pcm / K
    alpha_high_std = np.zeros_like(alpha_high)  # pcm / K
    alpha_low = np.zeros(len(T_matrix_low))               # pcm / K
    alpha_low_std = np.zeros_like(alpha_low)  # pcm / K
    print('\nalpha = 1/k dk/dT\n')
    T_cen = np.min(T_matrix_high)
    T_hig = np.max(T_matrix_high)
    T_low = np.min(T_matrix_low)
    for n in range(len(T_matrix_high)):
        alpha_high[n] = 1/k_eff[index_900]*(k_eff_high[n]-k_eff[index_900])/(T_hig-T_cen)*1E5
        alpha_high_std[n] = np.sqrt((k_eff_high[n]/k_eff[index_900]**2 * k_eff_std[index_900])**2 + (1/k_eff[index_900]* k_eff_std_high[n])**2)/(T_hig-T_cen)*1E5
        alpha_low[n] = 1/k_eff[index_900]*(k_eff[index_900] - k_eff_low[n])/(T_hig-T_cen)*1E5
        alpha_low_std[n] = np.sqrt((k_eff_low[n]/k_eff[index_900]**2 * k_eff_std[index_900])**2 + (1/k_eff[index_900]* k_eff_std_low[n])**2)/(T_cen-T_low)*1E5
        print('alpha high {} = {:.2f} +/- {:.2f} pcm/K'.format(n,alpha_high[n],alpha_high_std[n]))
        print('alpha low {} = {:.2f} +/- {:.2f} pcm/K\n'.format(n,alpha_low[n],alpha_low_std[n]))
        plt.errorbar([T_low,T_cen,T_hig],np.array([rho_low[n],rho[index_900],rho_high[n]])*1E5,np.array([rho_std_low[n],rho_std[index_900],rho_std_high[n]])*1E5,fmt='o-',color=colors_1[n],capsize=5,label='$'+f'T_{n}'+'$ '+labels[n])

    alpha_high_sum = np.sum(alpha_high)
    alpha_high_sum_std = np.sqrt(np.sum(alpha_high_std**2))
    alpha_low_sum = np.sum(alpha_low)
    alpha_low_sum_std = np.sqrt(np.sum(alpha_low_std**2))
    plt.errorbar([T_low,T_hig],np.array([np.sum(rho_low-rho[index_900])+rho[index_900],np.sum(rho_high-rho[index_900])+rho[index_900]])*1E5,np.array([np.sqrt(np.sum(rho_std_low**2))*1E5,np.sqrt(np.sum(rho_std_high**2))*1E5]),fmt='o',color=colors_1[6],capsize=5,label='$T_{sum}$')

    plt.legend()
    print('sum alpha high = {:.2f} +/- {:.2f} pcm/K'.format(alpha_high_sum,alpha_high_sum_std))
    print('sum alpha low = {:.2f} +/- {:.2f} pcm/K'.format(alpha_low_sum,alpha_low_sum_std))
    
    # total alpha
    alpha_high_total = 1/k_eff[index_900]*(k_eff[index_950]-k_eff[index_900])/(T_hig-T_cen)*1E5
    alpha_high_total_std = np.sqrt((k_eff[index_950]/k_eff[index_900]**2 * k_eff_std[index_900])**2 + (1/k_eff[index_900]* k_eff_std[index_950])**2)/(T_hig-T_cen)*1E5
    alpha_low_total = 1/k_eff[index_900]*(k_eff[index_900]-k_eff[index_850])/(T_cen-T_low)*1E5
    alpha_low_total_std = np.sqrt((k_eff[index_850]/k_eff[index_900]**2 * k_eff_std[index_900])**2 + (1/k_eff[index_900]* k_eff_std[index_850])**2)/(T_cen-T_low)*1E5
    print('total alpha high = {:.2f} +/- {:.2f} pcm/K'.format(alpha_high_total,alpha_high_total_std))
    print('total alpha low = {:.2f} +/- {:.2f} pcm/K\n'.format(alpha_low_total,alpha_low_total_std))
    
    print(' , alpha_low (pcm/K), alpha_high (pcm/K)')
    for n in range(5):
        print('alpha_{}, {:.2f} +/- {:.2f}, {:.2f} +/- {:.2f}'.format(n,alpha_low[n],alpha_low_std[n],alpha_high[n],alpha_high_std[n]))
    print('sum, {:.2f} +/- {:.2f}, {:.2f} +/- {:.2f}'.format(alpha_low_sum,alpha_low_sum_std,alpha_high_sum,alpha_high_sum_std))
    print('direct total, {:.2f} +/- {:.2f}, {:.2f} +/- {:.2f}'.format(alpha_low_total,alpha_low_total_std,alpha_high_total,alpha_high_total_std))
    
    print('\n\nnow for latex:')
    print(r' & $\alpha_{low}$ (pcm/K)& $\alpha_{high}$ (pcm/K) \\')
    print(r'\hline')
    for n in range(5):
        print(r'$\alpha_{}$ & {:.2f} $\pm$ {:.2f} & {:.2f} $\pm$ {:.2f} \\'.format(n,alpha_low[n],alpha_low_std[n],alpha_high[n],alpha_high_std[n]))
    print(r'\hline')
    print(r'$\sum_i \alpha_i$ & {:.2f} $\pm$ {:.2f}& {:.2f} $\pm$ {:.2f} \\'.format(alpha_low_sum,alpha_low_sum_std,alpha_high_sum,alpha_high_sum_std))
    print(r'\hline')
    print(r'$\alpha$ & {:.2f} $\pm$ {:.2f} & {:.2f} $\pm$ {:.2f}'.format(alpha_low_total,alpha_low_total_std,alpha_high_total,alpha_high_total_std))
    
    print(f'\n\n alpha_fuel_low = {alpha_low[0]+alpha_low[4]} +/- {np.sqrt((alpha_low_std[0])**2 + (alpha_low_std[4])**2)}')
    print(f'\n\n alpha_fuel_high = {alpha_high[0]+alpha_high[4]} +/- {np.sqrt((alpha_high_std[0])**2 + (alpha_high_std[4])**2)}')

def PlotConvergence():
    folder_name, T_matrix, (T_matrix_global, T_matrix_high, T_matrix_low) = GetInputParameters()
    fig,ax = plt.subplots(dpi=150)
    for n,T_vec in enumerate(T_matrix):
        file_name = 'input_file_T0={:.2f}K_T1={:.2f}K_T2={:.2f}K_T3={:.2f}K_T4={:.2f}K_T5={:.2f}K.in_his0.m'.format(*T_vec)
        file_path = os.path.join(folder_name,file_name)
        data = serpentTools.read(file_path)
        k_eff_impl = data.arrays['anaKeff'][:,1]
        k_eff_impl_std = data.arrays['anaKeff'][:,2]*k_eff_impl
        ax.errorbar(np.arange(len(k_eff_impl))[::100],k_eff_impl[::100],yerr=k_eff_impl_std[::100],label='{} K'.format(T_vec[0]),capsize=2)
    ax.set_xlabel('cycles')
    ax.set_ylabel('k_eff_implicit') 
    leg = fig.legend()
    leg.set_draggable(True)
    
if __name__ == '__main__':
    EvaluateResults()
    #PlotConvergence()