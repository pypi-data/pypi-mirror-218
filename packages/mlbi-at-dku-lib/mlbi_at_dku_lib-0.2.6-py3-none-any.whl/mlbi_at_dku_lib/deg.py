import time, os, copy, datetime, math, random, warnings
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from statannot import add_stat_annotation
import matplotlib.pyplot as plt
from matplotlib import cm


from importlib_resources import files

def load_GTmap( target = 'hg38' ):
    
    if target in ['hg38', 'hg19', 'mm10']:
        path = files('mlbi_at_dku_lib.data').joinpath('GTmap_%s.csv' % target)
        return pd.read_csv(path, index_col = 0)
    else:
        print('ERROR: cannot find the data file %s.' % ('GTmap_%s.csv' % target))
        print('You can choose one of hg38, hg19, mm10')
        return None
    
    return None


### Example 
# df_cnt, df_pct= get_population( adata_s.obs['sid'], 
#                                 adata_s.obs['minor'], sort_by = [] )
# plot_population(df_pct, figsize=(6, 4), dpi = 80, return_fig = False)
# df_cnt
    
def get_population( pids, cts, sort_by = [] ):
    
    pid_lst = list(set(list(pids)))
    pid_lst.sort()
    celltype_lst = list(set(list(cts)))
    celltype_lst.sort()

    df_celltype_cnt = pd.DataFrame(index = pid_lst, columns = celltype_lst)
    df_celltype_cnt.loc[:,:] = 0

    for pid in pid_lst:
        b = np.array(pids) == pid
        ct_sel = np.array(cts)[b]

        for ct in celltype_lst:
            bx = ct_sel == ct
            df_celltype_cnt.loc[pid, ct] = np.sum(bx)

    df_celltype_pct = (df_celltype_cnt.div(df_celltype_cnt.sum(axis = 1), axis = 0)*100).astype(float)
    
    if len(sort_by) > 0:
        df_celltype_pct.sort_values(by = sort_by, inplace = True)

    return df_celltype_cnt, df_celltype_pct


def plot_population(df_pct, title = None, title_fs = 12, 
                    label_fs = 11, tick_fs = 10, tick_rot = 45,
                    legend_fs = 10, legend_loc = 'upper left', bbox_to_anchor = (1,1), 
                    legend_ncol = 1, cmap_name = None, figsize=(5, 3), return_fig = False):    

    if cmap_name is None:
        cmap_name = 'Spectral'
    cmap = plt.get_cmap(cmap_name)
    color = cmap(np.arange(df_pct.shape[1])/df_pct.shape[1])
    
    ax = df_pct.plot.bar(stacked = True, rot = tick_rot, figsize = figsize, color = color)
    ax.legend( list(df_pct.columns.values), bbox_to_anchor=bbox_to_anchor, 
               loc = legend_loc, fontsize = legend_fs, ncol = legend_ncol )
    plt.xticks(fontsize=tick_fs)
    plt.yticks(fontsize=tick_fs)
    plt.ylabel('Percentage [%]', fontsize = label_fs)
    plt.title(title, fontsize = title_fs)
    if return_fig:
        return ax
    else:
        plt.show()
        return
    return


def plot_population_g(df_pct, sg_map, sort_by = [], title = None, title_y = 1.05, title_fs = 14, 
                    title_fs2 = 12, label_fs = 11, tick_fs = 10, tick_rot = 45,
                    legend_fs = 10, legend_loc = 'upper left', bbox_to_anchor = (1,1), 
                    legend_ncol = 1, cmap_name = None, figsize=(5, 3), return_fig = False):    

    if cmap_name is None:
        cmap_name = 'Spectral'
    cmap = plt.get_cmap(cmap_name)
    color = cmap(np.arange(df_pct.shape[1])/df_pct.shape[1])
    
    df = df_pct.copy(deep = True)

    items = list(df.columns.values)

    df['Group'] = list(df.index.values)
    df['Group'].replace(sg_map, inplace = True)

    num_p = []

    glst = list(df['Group'].unique())
    glst.sort()

    cnt = df['Group'].value_counts()
    for g in glst:
        num_p.append(cnt.loc[g])

    nr, nc = 1, len(glst)
    fig, axes = plt.subplots(nrows=nr, ncols=nc, constrained_layout=True, 
                             gridspec_kw={'width_ratios': num_p})
    fig.tight_layout() 
    if title is not None: 
        fig.suptitle(title, x = 0.5, y = title_y, fontsize = title_fs, ha = 'center')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.06, hspace=0.25)

    cnt = 0
    for j, g in enumerate(glst):
        b = df['Group'] == g
        dft = df.loc[b,:]
        if len(sort_by) > 0:
            dft = dft.sort_values(sort_by)
        ax = dft.plot.bar(width = 0.75, stacked = True, ax = axes[j+cnt], 
                          figsize = figsize, legend = None, color = color)
        ax.set_title('%s' % (g), fontsize = title_fs2)
        if j != 0:
            ax.set_yticks([])
        else:
            ax.set_ylabel('Proportion', fontsize = label_fs)

        ax.tick_params(axis='x', labelsize=tick_fs, rotation = tick_rot)
        ax.tick_params(axis='y', labelsize=tick_fs)
            
        if g == glst[-1]: 
            ax.legend(dft.columns.values, loc = legend_loc, bbox_to_anchor = bbox_to_anchor, 
                       fontsize = legend_fs, ncol = legend_ncol)  
        else:
            pass
    plt.show()
    
    return


def get_sample_to_group_dict( samples, conditions ):
    
    samples = np.array(samples)
    conditions = np.array(conditions)
    
    slst = list(set(list(samples)))
    slst.sort()
    glst = []
    for s in slst:
        b = samples == s
        g = conditions[b][0]
        glst.append(g)
        
    dct = dict(zip(slst, glst))
    return dct


def plot_pct_box(df_pct, sg_map, nr_nc, figsize = None, dpi = 100,
                 title = None, title_y = 1.05, title_fs = 14, 
                 title_fs2 = 12, label_fs = 11, tick_fs = 10, tick_rot = 0, 
                 annot_ref = None, annot_fmt = 'simple', annot_fs = 10, 
                 ws_hs = (0.3, 0.3)):
    
    df = df_pct.copy(deep = True)
    nr, nc = nr_nc
    ws, hs = ws_hs
    fig, axes = plt.subplots(figsize=figsize, dpi=dpi, nrows=nr, ncols=nc, constrained_layout=True)
    fig.tight_layout() # Or equivalently,  "plt.tight_layout()"
    if title is not None:
        fig.suptitle('%s' % title, x = 0.5, y = title_y, fontsize = title_fs, ha = 'center')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=ws, hspace=hs)

    items = list(df.columns.values)

    df['Group'] = list(df.index.values)
    df['Group'].replace(sg_map, inplace = True)

    lst = df['Group'].unique()
    lst_pair = []
    if annot_ref in lst:
        for k, l1 in enumerate(lst):
            if l1 != annot_ref:
                lst_pair.append((annot_ref, l1))
    else:
        for k, l1 in enumerate(lst):
            for j, l2 in enumerate(lst):
                if j >  k:
                    lst_pair.append((l1, l2))

    for k, item in enumerate(items):
        plt.subplot(nr,nc,k+1)
        ax = sns.boxplot(data = df, x = 'Group', y = item) #, order=['HC', 'CC', 'AC'])
        if k%nc == 0: plt.ylabel('Percentage', fontsize = label_fs)
        else: plt.ylabel(None)
        if k >= nc*(nr-1): plt.xlabel('Condition', fontsize = label_fs)
        else: plt.xlabel(None)
        plt.title(item, fontsize = title_fs2)
        if k < (nr*nc - nc):
            plt.xticks([])
            plt.yticks(fontsize = tick_fs)
        else:
            plt.xticks(rotation = tick_rot, ha = 'center', fontsize = tick_fs)
            plt.yticks(fontsize = tick_fs)
        
        add_stat_annotation(ax, data=df, x = 'Group', y = item, 
                        box_pairs=lst_pair, loc='inside', fontsize = annot_fs,
                        test='t-test_ind', text_format=annot_fmt, verbose=0)
        #'''
    if (len(items) < (nr*nc)) & (nr > 1):
        for k in range(nr*nc - len(items)):
            axes[nr-1][len(items)%nc + k].axis("off")
        
    plt.show()
    return 


def plot_pct_box_old(df_pct, sg_map, nr_nc, figsize = None, dpi = 100,
                 title = None, title_y = 1.05, title_fs = 14, 
                 title_fs2 = 12, label_fs = 11, tick_fs = 10, tick_rot = 0, 
                 annot_fs = 10, ws_hs = (0.3, 0.3)):
    
    df = df_pct.copy(deep = True)
    nr, nc = nr_nc
    ws, hs = ws_hs
    fig, axes = plt.subplots(figsize=figsize, dpi=dpi, nrows=nr, ncols=nc, constrained_layout=True)
    fig.tight_layout() # Or equivalently,  "plt.tight_layout()"
    if title is not None:
        fig.suptitle('%s' % title, x = 0.5, y = title_y, fontsize = title_fs, ha = 'center')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=ws, hspace=hs)

    items = list(df.columns.values)

    df['Group'] = list(df.index.values)
    df['Group'].replace(sg_map, inplace = True)

    lst = df['Group'].unique()
    lst_pair = []
    for k, l1 in enumerate(lst):
        for j, l2 in enumerate(lst):
            if j >  k:
                lst_pair.append((l1, l2))

    for k, item in enumerate(items):
        plt.subplot(nr,nc,k+1)
        ax = sns.boxplot(data = df, x = 'Group', y = item) #, order=['HC', 'CC', 'AC'])
        if k%nc == 0: plt.ylabel('Percentage', fontsize = label_fs)
        else: plt.ylabel(None)
        if k >= nc*(nr-1): plt.xlabel('Condition', fontsize = label_fs)
        else: plt.xlabel(None)
        plt.title(item, fontsize = title_fs2)
        if k < (nr*nc - nc):
            plt.xticks([])
            plt.yticks(fontsize = tick_fs)
        else:
            plt.xticks(rotation = 0, ha = 'center', fontsize = tick_fs)
            plt.yticks(fontsize = tick_fs)

        add_stat_annotation(ax, data=df, x = 'Group', y = item, # order=['HC', 'CC', 'AC'],
                        box_pairs=lst_pair, loc='inside', fontsize = annot_fs,
                        test='t-test_ind', text_format='simple', verbose=0)
        #'''
    if (len(items) < (nr*nc)) & (nr > 1):
        for k in range(nr*nc - len(items)):
            axes[nr-1][len(items)%nc + k].axis("off")
        
    plt.show()
    return


######## DEG ##########

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