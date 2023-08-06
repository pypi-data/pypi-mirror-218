import pandas as pd
import scanpy as sc
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, facecolor='white',fontsize=12)
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager
import matplotlib.font_manager as fm
import anndata

def create_loc(meta_df):
    df = pd.DataFrame(0,index=range(1),columns=range(len(meta_df.iloc[:,5:].columns)))
    df.columns = pd.MultiIndex.from_tuples(meta_df.iloc[:,5:].columns.str.split('_').map(tuple))
    df = df.stack()
    df = df.reset_index()
    df.index = df["level_1"]
    df = df.iloc[:,2:]
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    return df

def transform(df):
    df = df.fillna(0)
    df.index = df.index.str[1:].astype(int)
    df.columns = df.columns.str[1:].astype(int)
    df = df.sort_index(axis=0)
    df = df.sort_index(axis=1)
    return df

import pandas as pd
import scanpy as sc
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, facecolor='white',fontsize=12)
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager
import matplotlib.font_manager as fm

def create_loc(meta_df):
    df = pd.DataFrame(0,index=range(1),columns=range(len(meta_df.iloc[:,5:].columns)))
    df.columns = pd.MultiIndex.from_tuples(meta_df.iloc[:,5:].columns.str.split('_').map(tuple))
    df = df.stack()
    df = df.reset_index()
    df.index = df["level_1"]
    df = df.iloc[:,2:]
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    return df

def transform(df):
    df = df.fillna(0)
    df.index = df.index.str[1:].astype(int)
    df.columns = df.columns.str[1:].astype(int)
    df = df.sort_index(axis=0)
    df = df.sort_index(axis=1)
    return df


def umap_projection(adata_name, file_name='', leiden_key_added='leiden', pltcmap='',figtitle='',figdpi=100, fig_size=(5,4), add_scalebar=True):
    loc_df = create_loc(file_name)
    num_celltype = len(set(adata_name.obs[leiden_key_added]))
    df = adata_name.obs
    for i in range(1,num_celltype+1): ##changed
        tmp = df[df[leiden_key_added] == str(i)].index.str.split('_').tolist() ##changed
        for idx in tmp:
            loc_df.loc[idx[1],idx[0]] = i
    loc_df = transform(loc_df)

    fig, (ax1,axcb1) = plt.subplots(1,2, figsize = fig_size,dpi = figdpi, gridspec_kw={'width_ratios':[1,0.05]})

    g1 = sns.heatmap(loc_df,
                     mask=(loc_df==0),cmap=pltcmap,
                     cbar_kws={"shrink": 0.5,"ticks":list(range(1,num_celltype+1))},
                     ax=ax1,cbar_ax=axcb1)
    g1.set_title(figtitle, fontsize=14)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    
    if add_scalebar==True:
        scalebar1 = AnchoredSizeBar(ax1.transData, 30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                               fontproperties=fm.FontProperties(size=8))
        ax1.add_artist(scalebar1)
    plt.show()
    
def umap_projection_subset(adata_name, file_name='', leiden_key_added='leiden', pltcmap='',figtitle='',figdpi=100, fig_size=(5,4),
                           subset=[95,185,35,175]):
    loc_df = create_loc(file_name)
    num_celltype = len(set(adata_name.obs[leiden_key_added]))
    df = adata_name.obs
    for i in range(1,num_celltype+1): ##changed
        tmp = df[df[leiden_key_added] == str(i)].index.str.split('_').tolist() ##changed
        for idx in tmp:
            loc_df.loc[idx[1],idx[0]] = i
    loc_df = transform(loc_df)
    loc_df=loc_df.iloc[subset[0]:subset[1], subset[2]:subset[3]]
    fig, ax1 = plt.subplots(1,1, figsize = fig_size, dpi = figdpi)
    g1 = sns.heatmap(loc_df,
                     mask=(loc_df==0),cmap=pltcmap,
                     ax=ax1,cbar=False)
    g1.set_title(figtitle, fontsize=14)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    
    plt.show()
    
def project3tissues(raw_file1,raw_file2,raw_file3, adata_name, leiden_key='leiden',suffix1='data1',suffix2='data2',suffix3='data3',
                    cmap = "magma_r",figdpi=100, fig_size=(15,5), add_scalebar=True,
                   subtitle1='',subtitle2='',subtitle3=''):
    file1_df = create_loc(raw_file1)
    file2_df = create_loc(raw_file2)
    file3_df = create_loc(raw_file3)
    num_celltype=len(set(adata_name.obs[leiden_key]))
    df = adata_name.obs
    for i in range(1,num_celltype+1):
        tmp = df[df[leiden_key] == str(i)].index.str.split('_').tolist()
        for idx in tmp:
            if idx[2] == suffix1:
                file1_df.loc[idx[1],idx[0]] = i
            elif idx[2] == suffix2:
                file2_df.loc[idx[1],idx[0]] = i
            elif idx[2] == suffix3:
                file3_df.loc[idx[1],idx[0]] = i

    df1 = transform(file1_df)
    df2 = transform(file2_df)
    df3 = transform(file3_df)

    fig, ((ax1,ax2,ax3,axcb1)) = plt.subplots(1, 4, figsize = fig_size,dpi = figdpi,gridspec_kw={'width_ratios':[1,1,1,0.05]})

    g1 = sns.heatmap(df1,
                    mask=(df1==0),cmap=cmap,
                    ax=ax1,cbar=False)
    g1.set_title(subtitle1,fontsize=16)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])

    g2 = sns.heatmap(df2,
                     mask=(df2==0),cmap=cmap,
                     ax=ax2,cbar=False)
    g2.set_title(subtitle2,fontsize=16)
    g2.set_ylabel('');g2.set_xlabel('');g2.set_xticks([]);g2.set_yticks([])

    g3 = sns.heatmap(df3,
                     mask=(df3==0),cmap=cmap,
                     cbar_kws={"shrink": 0.5,"ticks":list(range(1,num_celltype+1))},
                     ax=ax3,cbar_ax=axcb1)
    g3.set_title(subtitle3,fontsize=16)
    g3.set_ylabel('');g3.set_xlabel('');g3.set_xticks([]);g3.set_yticks([])
    
    #plt.suptitle(title, fontsize = 14)
    if add_scalebar==True:
        scalebar1 = AnchoredSizeBar(ax1.transData,30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                                   fontproperties=fm.FontProperties(size=10))
        scalebar2 = AnchoredSizeBar(ax2.transData, 30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                                   fontproperties=fm.FontProperties(size=10))
        scalebar3 = AnchoredSizeBar(ax3.transData, 30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                                   fontproperties=fm.FontProperties(size=10))
        ax1.add_artist(scalebar1);ax2.add_artist(scalebar2);ax3.add_artist(scalebar3)
    plt.show()
    
def add_coords(adata):
    x_coords=[]
    y_coords=[]
    for i in adata.obs.index:
        x1=i.split('_')[0].split('x')[1]
        y1=i.split('_')[1].split('y')[1]
        x_coords.append(int(x1))
        y_coords.append(int(y1))
    adata.obs['x_coords']=x_coords
    adata.obs['y_coords']=y_coords
    return adata

def project_cluster_in_groups(adata, cluster_id, cluster_obs_name, group_list, group_obs_name, cmap='Greys'):
    
    print("Cluster: ", cluster_id)
    fig, axes = plt.subplots(1, len(group_list), figsize = (5*len(group_list),5), dpi = 300)
    df_dict = {}
    for g in group_list:
        sub_ad = adata[(adata.obs[group_obs_name] == g) & (adata.obs[cluster_obs_name] == str(cluster_id))]
        loc_df = sub_ad.obs[["x_coords","y_coords"]].copy()
        M = loc_df["y_coords"].max() + 1
        N = loc_df["x_coords"].max() + 1
        loc_df["values"] = 1
        loc_df.set_index(["y_coords", "x_coords"], inplace=True)
        index = pd.MultiIndex.from_product([range(M), range(N)], names=['y_coords', 'x_coords'])
        df_zero = loc_df.reindex(index, fill_value=-1)['values'].unstack()
        df_zero.rename_axis(index=None, columns=None, inplace=True)
        df_dict[g] = df_zero
    
    axes = axes.flatten()
    
    for idx, g in enumerate(group_list):
        plt_df = df_dict[g]
        sns.heatmap(plt_df, cmap=cmap, ax=axes[idx], cbar=False)
        axes[idx].set_xticks([])
        axes[idx].set_yticks([])
        axes[idx].set_facecolor("white")
    
    plt.tight_layout()
    
    return fig