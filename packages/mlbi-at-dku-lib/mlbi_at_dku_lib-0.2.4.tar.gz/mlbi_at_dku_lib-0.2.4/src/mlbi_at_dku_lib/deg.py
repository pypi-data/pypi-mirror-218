import time, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats

MIN_VALUE = 1e-10
MIN_VALUE_EF = 1e-10

def perform_deg( df_cbyg_in, groups, target_group, min_ef = 0.05, exp_only = False ):
    
    # b = groups == ref_group
    b = groups != target_group
    
    b1 = (df_cbyg_in.loc[~b,:] > 0).mean(axis = 0) >= min_ef 
    b2 = (df_cbyg_in.loc[b,:] > 0).mean(axis = 0) >= min_ef 
    bx = b1 | b2
    df_cbyg = (df_cbyg_in).loc[:,bx]
    
    g_mec_ref = (df_cbyg.loc[b,:] > 0).mean(axis = 0)
    g_mec_test = (df_cbyg.loc[~b,:] > 0).mean(axis = 0)
    
    eft = (g_mec_test)
    efr = (g_mec_ref)
    efc = (eft + MIN_VALUE_EF)/(efr + MIN_VALUE_EF)
    
    df = pd.DataFrame(index = df_cbyg.columns)
    
    df['EFC'] = list(efc)
    df['log10_EFC'] = list(np.round(np.log10(efc), 3))
    df['EF_test'] = list(eft)
    df['EF_ref'] = list(efr)
    # df['Score'] = df['log10_EFC']*(np.sum(~b)*eft + np.sum(b)*efr)
        
    #'''
    g_mean_ref = df_cbyg.loc[b,:].mean(axis = 0)
    g_mean_test = df_cbyg.loc[~b,:].mean(axis = 0)
    g_std_ref = df_cbyg.loc[b,:].std(axis = 0)
    g_std_test = df_cbyg.loc[~b,:].std(axis = 0)

    if exp_only: 
        g_mean_ref = g_mean_ref/(efr + MIN_VALUE)
        g_mean_test = g_mean_test/(eft + MIN_VALUE)
        g_std_ref = g_std_ref/np.sqrt(efr + MIN_VALUE)
        g_std_test = g_std_test/np.sqrt(eft + MIN_VALUE)
    
    # fc = (g_mean_test + MIN_VALUE)/(g_mean_ref + MIN_VALUE)
    fc = (np.expm1(g_mean_test) + MIN_VALUE)/(np.expm1(g_mean_ref) + MIN_VALUE)
    stat = np.abs(g_mean_test - g_mean_ref)
    
    if exp_only: 
        stat = stat/((g_std_ref/np.sqrt(np.sum(b)*efr + MIN_VALUE)) \
                    + g_std_test/np.sqrt(np.sum(~b)*eft + MIN_VALUE))
    else:
        stat = stat/(g_std_ref/np.sqrt(np.sum(b) + MIN_VALUE) \
                   + g_std_test/np.sqrt(np.sum(~b) + MIN_VALUE))
        
    df['mean_test'] = list(g_mean_test)
    df['mean_ref'] = list(g_mean_ref)
    df['log2_FC'] = list(np.round(np.log2(fc), 3))
    
    if exp_only:
        pv = stats.t.sf(stat*np.sqrt(2), df = (np.sum(b)*efr + np.sum(~b)*eft)-2)*2
    else:
        pv = stats.t.sf(stat*np.sqrt(2), df = (np.sum(b)*efr + np.sum(~b)*eft)-2)*2
        # pv = stats.t.sf(stat, df = np.sum(b)-2)*2
    pv = pv 
        
    pv_adj = pv * df_cbyg.shape[1]
    df['pval'] = list(pv)
    df['pval_adj'] = list(pv_adj)
    df['pval_adj'].clip(upper = 1, inplace = True)
    #'''
    df = df.sort_values(by = 'EFC', ascending = False)
        
    return df


def deg_multi( df_cbyg_in, groups_in, ref_group = None, samples_in = None,
               min_ef = 0.05, exp_only = False, min_frac = 0.1 ):

    glst = list(set(list(groups_in)))
    glst.sort()
    
    if not isinstance(groups_in, pd.Series):
        groups_in = pd.Series(groups_in, index = df_cbyg_in.index.values)

    df_lst = {}
    for g in glst:

        if (ref_group is None):
            groups = groups_in.copy(deep = True).astype(str)
            ref_g = 'others'
            b = groups != g
            groups[b] = ref_group
            df_cbyg = df_cbyg_in
        else:
            if ref_group == g:
                groups = groups_in.copy(deep = True).astype(str)
                ref_g = 'others'
                b = groups != g
                groups[b] = ref_g
                df_cbyg = df_cbyg_in
            else:
                ref_g = ref_group
                b = groups_in.isin([g, ref_group])
                groups = groups_in[b]
                df_cbyg = df_cbyg_in.loc[b,:]

        df_deg = perform_deg( df_cbyg, groups, target_group = g, 
                              min_ef = min_ef, exp_only = exp_only )
        key = '%s_vs_%s' % (g, ref_g)
        df_lst[key] = df_deg

        if samples_in is not None:
            if len(samples_in) == df_cbyg_in.shape[0]:
                b = groups_in == g
                dft = find_fraction_of_patients_for_vaild_marker_exp( df_lst[key], 
                            df_cbyg_in.loc[b,:], pids = samples_in[b], min_frac = min_frac )
                df_lst[key]['Rp'] = dft['Rp'] 
        
    return df_lst


def find_fraction_of_patients_for_vaild_marker_exp( df_deg, df_cbyg, pids, min_frac = 0.1 ):
    
    dft = pd.DataFrame(index = df_deg.index) 
    dft['Rp'] = 0
    X = df_cbyg

    glst = list(dft.index.values)
    plst= list(set(list(pids)))
    
    for p in plst:
        bp = pids == p
        exp_frac = (X.loc[bp, glst] > 0).mean(axis = 0)

        dft['Rp'] += list(exp_frac >= min_frac)

    dft['Rp'] = np.round(dft['Rp']/len(plst), 3)
    
    return dft

def get_fraction_of_samples_for_vaild_marker( df_lst, df_cbyg, groups, samples, min_frac = 0.1 ):

    for key in df_lst.keys():

        subtype = key.split('_')[0]
        b = groups == subtype

        ## For each markers, get percentage of patient who has the marker expressed 
        dft = find_fraction_of_patients_for_vaild_marker_exp( df_lst[key], df_cbyg.loc[b,:], 
                                                              pids = samples[b], min_frac = min_frac )
        ## fraction of patient who has the corresponding marker expressed
        df_lst[key]['Rp'] = dft['Rp'] 

    return df_lst