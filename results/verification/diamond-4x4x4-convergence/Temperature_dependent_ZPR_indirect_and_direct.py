#!/usr/bin/env python3
# coding: utf-8

# In[2]:


import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
# from sklearn.linear_model import LinearRegression
mpl.rcParams['figure.dpi']= 200
# get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
# plt.rcParams['font.size'] = 15
# mpl.rcParams['axes.linewidth'] = 2

RYTOEV = 13.605698 # Rydberg to eV
ryd2mev = RYTOEV*1000


# In[3]:


# get_ipython().system('ls')


# In[4]:


# Kresse 
kresse_dft = pd.read_csv("./ref-data/2018-Kresse-NJP-fig5-4x4x4-DFT.csv")
kresse_gw = pd.read_csv("./ref-data/2018-Kresse-NJP-fig5-4x4x4-GW.csv")
kresse_dft_indirect = pd.read_csv("./ref-data/2018-Kresse-NJP-fig6-5x5x5-DFT.csv")
kresse_dft_indirect["gap"] = (kresse_dft_indirect["gap"]-kresse_dft_indirect["gap"].values[0])*1000

# Antonius 2014
antonius_dfpt = pd.read_csv("./ref-data/2014-Antonius-PRL-fig3-DFPT.csv")
antonius_dfpt["zpr"] = ( antonius_dfpt["gap"] - antonius_dfpt["gap"].values[0] ).values * 1000

antonius_dfpt_gw = pd.read_csv("./ref-data/2014-Antonius-PRL-fig3-DFPT+GW.csv")
antonius_dfpt_gw["zpr"] = ( antonius_dfpt_gw["gap"] - antonius_dfpt_gw["gap"].values[0] ).values * 1000

# Bartomeu Monserrat, PHYSICAL REVIEW B 93, 100301(R) (2016)
monserrat_dfpt = pd.read_csv("./ref-data/2016-Monserrat-PRB-DFPT.csv")
monserrat_dfpt_gw = pd.read_csv("./ref-data/2016-Monserrat-PRB-DFPT+GW.csv")

monserrat_dfpt["zpr"] = ( monserrat_dfpt["zpr"] - monserrat_dfpt["zpr"].values[0]).values
monserrat_dfpt_gw["zpr"] = ( monserrat_dfpt_gw["zpr"] - monserrat_dfpt_gw["zpr"].values[0]).values

# Arpan's frozen phonon calculations with 128 atoms
arpan_fp_128 = pd.read_csv("./ref-data/2021-Arpan-128.csv")
arpan_fp_128["edge"] = ( arpan_fp_128["edge"] - arpan_fp_128["edge"].values[0] ) * 1000
arpan_fp_128["center"] = ( arpan_fp_128["center"] - arpan_fp_128["center"].values[0] ) * 1000


# Experimental direct gap extracted from
# S. Logothetidis, J. Petalas, H. M. Polatoglou, and D. Fuchs
# Phys. Rev. B 46, 4483
gapA1 = pd.read_csv("./ref-data/gapA1.csv")
gapA2 = pd.read_csv("./ref-data/gapA2.csv")
gapB1 = pd.read_csv("./ref-data/gapB1.csv")
gapB2 = pd.read_csv("./ref-data/gapB2.csv")
fitted = pd.read_csv("./ref-data/fitted.csv")
errorbar = pd.read_csv("./ref-data/errorbar.csv")


# extract fitted gap at zero
fitted["Eb-aB"] = fitted["Eb"]-fitted["aB"]
gapA1["gap"] = gapA1["gap"] - fitted[fitted["Data"]=="A1"]["Eb-aB"].values[0]
gapA2["gap"] = gapA2["gap"] - fitted[fitted["Data"]=="A2"]["Eb-aB"].values[0]
gapB1["gap"] = gapB1["gap"] - fitted[fitted["Data"]=="B1"]["Eb-aB"].values[0]
gapB2["gap"] = gapB2["gap"] - fitted[fitted["Data"]=="B2"]["Eb-aB"].values[0]


# eV to meV
gapA1["gap"] = gapA1["gap"]*1000
gapA2["gap"] = gapA2["gap"]*1000
gapB1["gap"] = gapB1["gap"]*1000
gapB2["gap"] = gapB2["gap"]*1000

## Indirect gap ZPR
chen = pd.read_csv("./ref-data/1991-Chen-Diamond-Indirect-ZPR.csv")
chen["gap"] = ( chen["gap"] - chen["gap"].values[0] ) * 1000


# In[5]:


def extract_gamma_direct_zpr(prefix,vbm,cbm,enable_gw=False):
    zpr_dft = 0
    zpr_gw  = 0
    fmfname = prefix +"/reFMselfen_DFT_adi.tab"
    dwfname = prefix +"/reDWselfen_DFT.tab"
    fm_dft = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    dw_dft = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    vbm_zpr_dft = fm_dft[np.logical_and(fm_dft["ibn"]==vbm,fm_dft["iks"]==1)]["re"].values[0] + dw_dft[np.logical_and(dw_dft["ibn"]==vbm,dw_dft["iks"]==1)]["re"].values[0]
    cbm_zpr_dft = fm_dft[np.logical_and(fm_dft["ibn"]==cbm,fm_dft["iks"]==1)]["re"].values[0] + dw_dft[np.logical_and(dw_dft["ibn"]==cbm,dw_dft["iks"]==1)]["re"].values[0]
    zpr_dft = cbm_zpr_dft - vbm_zpr_dft

    if ( enable_gw ):
        fmfname = prefix +"/reFMselfen_eqpgw_adi.tab"
        dwfname = prefix +"/reDWselfen_eqpgw.tab"
        fm_gw = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        dw_gw = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        vbm_zpr_gw = fm_gw[np.logical_and(fm_gw["ibn"]==vbm,fm_gw["iks"]==1)]["re"].values[0] + dw_gw[np.logical_and(dw_gw["ibn"]==vbm,dw_gw["iks"]==1)]["re"].values[0]
        cbm_zpr_gw = fm_gw[np.logical_and(fm_gw["ibn"]==cbm,fm_gw["iks"]==1)]["re"].values[0] + dw_gw[np.logical_and(dw_gw["ibn"]==cbm,dw_gw["iks"]==1)]["re"].values[0]
        zpr_gw = cbm_zpr_gw - vbm_zpr_gw
    return zpr_dft, zpr_gw

def extract_indirect_zpr(prefix,vbm,cbm,enable_gw=False):
    zpr_dft = 0
    zpr_gw  = 0
    fmfname = prefix +"/reFMselfen_DFT_adi.tab"
    dwfname = prefix +"/reDWselfen_DFT.tab"
    fm_dft = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    dw_dft = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    vbm_zpr_dft = fm_dft[fm_dft["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0] + dw_dft[dw_dft["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0]
    cbm_zpr_dft = fm_dft[fm_dft["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0] + dw_dft[dw_dft["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0]
    zpr_dft = cbm_zpr_dft - vbm_zpr_dft

    if ( enable_gw ):
        fmfname = prefix +"/reFMselfen_eqpgw_adi.tab"
        dwfname = prefix +"/reDWselfen_eqpgw.tab"
        fm_gw = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        dw_gw = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        vbm_zpr_gw = fm_gw[fm_gw["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0] + dw_gw[dw_gw["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0]
        cbm_zpr_gw = fm_gw[fm_gw["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0] + dw_gw[dw_gw["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0]
        zpr_gw = cbm_zpr_gw - vbm_zpr_gw
    return zpr_dft, zpr_gw

# prefix = "./60Ry/c.welph.save.pdep200.T0"
# zpr_indirect_lda, zpr_indirect_gw = extract_indirect_zpr(prefix,vbm=4,cbm=5,enable_gw=False)
# zpr_direct_lda, zpr_direct_gw = extract_gamma_direct_zpr(prefix,vbm=4,cbm=5,enable_gw=False)
# print(zpr_indirect_lda)
# print(zpr_direct_lda)


# ## Read ZPRs computed with LDA functional

# In[6]:


# Antonius lattice structure
T_lda = [0,100,200,300,400,500,600,700]
zprs_direct_lda = []
zprs_direct_lda_gw = []
for t in T_lda:
    prefix = "./60Ry/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_gamma_direct_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_direct_lda.append(tmp[0])
    zprs_direct_lda_gw.append(tmp[1])

zprs_direct_lda = np.array(zprs_direct_lda) - zprs_direct_lda[0]
zprs_direct_lda_gw = np.array(zprs_direct_lda_gw) - zprs_direct_lda_gw[0]
print(zprs_direct_lda)
print(zprs_direct_lda_gw)

T_lda = [0,100,200,300,400,500,600,700]
zprs_indirect_lda = []
zprs_indirect_lda_gw = []
for t in T_lda:
    prefix = "./60Ry/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_indirect_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_indirect_lda.append(tmp[0])
    zprs_indirect_lda_gw.append(tmp[1])

zprs_indirect_lda = np.array(zprs_indirect_lda) - zprs_indirect_lda[0]
zprs_indirect_lda_gw = np.array(zprs_indirect_lda_gw) - zprs_indirect_lda_gw[0]
print(zprs_indirect_lda)
print(zprs_indirect_lda_gw)


# ## Read ZPRs computed with PBE functional (Kresse lattice)

# In[7]:


T_lda = [0,100,200,300,400,500,600,700]
zprs_direct_pbe_kr = []
zprs_direct_pbe_gw_kr = []
for t in T_lda:
    prefix = "./60Ry-PBE-Kresse/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_gamma_direct_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_direct_pbe_kr.append(tmp[0])
    zprs_direct_pbe_gw_kr.append(tmp[1])

zprs_direct_pbe_kr = np.array(zprs_direct_pbe_kr) - zprs_direct_pbe_kr[0]
zprs_direct_pbe_gw_kr = np.array(zprs_direct_pbe_gw_kr) - zprs_direct_pbe_gw_kr[0]

print(zprs_direct_pbe_kr)
print(zprs_direct_pbe_gw_kr)

T_pbe = [0,100,200,300,400,500,600,700]
zprs_indirect_pbe_kr = []
zprs_indirect_pbe_gw_kr = []
for t in T_lda:
    prefix = "./60Ry-PBE-Kresse/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_indirect_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_indirect_pbe_kr.append(tmp[0])
    zprs_indirect_pbe_gw_kr.append(tmp[1])

zprs_indirect_pbe_kr = np.array(zprs_indirect_pbe_kr) - zprs_indirect_pbe_kr[0]
zprs_indirect_pbe_gw_kr = np.array(zprs_indirect_pbe_gw_kr) - zprs_indirect_pbe_gw_kr[0]

print(zprs_indirect_pbe_kr)
print(zprs_indirect_pbe_gw_kr)


# ## Read ZPRs computed with PBE functional (Relaxed lattice)

# In[8]:


T_lda = [0,100,200,300,400,500,600,700]
zprs_direct_pbe_rlx = []
zprs_direct_pbe_gw_rlx = []
for t in T_lda:
    prefix = "./60Ry-PBE-myrelax/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_gamma_direct_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_direct_pbe_rlx.append(tmp[0])
    zprs_direct_pbe_gw_rlx.append(tmp[1])

zprs_direct_pbe_rlx = np.array(zprs_direct_pbe_rlx) - zprs_direct_pbe_rlx[0]
zprs_direct_pbe_gw_rlx = np.array(zprs_direct_pbe_gw_rlx) - zprs_direct_pbe_gw_rlx[0]

print(zprs_direct_pbe_rlx)
print(zprs_direct_pbe_gw_rlx)

T_pbe = [0,100,200,300,400,500,600,700]
zprs_indirect_pbe_rlx = []
zprs_indirect_pbe_gw_rlx = []
for t in T_lda:
    prefix = "./60Ry-PBE-myrelax/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_indirect_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_indirect_pbe_rlx.append(tmp[0])
    zprs_indirect_pbe_gw_rlx.append(tmp[1])

zprs_indirect_pbe_rlx = np.array(zprs_indirect_pbe_rlx) - zprs_indirect_pbe_rlx[0]
zprs_indirect_pbe_gw_rlx = np.array(zprs_indirect_pbe_gw_rlx) - zprs_indirect_pbe_gw_rlx[0]

print(zprs_indirect_pbe_rlx)
print(zprs_indirect_pbe_gw_rlx)


# ## Read ZPRs computed with PBE functional (Arpan lattice)

# In[9]:


T_lda = [0,100,200,300,400,500,600,700]
zprs_direct_pbe_ar = []
zprs_direct_pbe_gw_ar = []
for t in T_lda:
    prefix = "./60Ry-PBE-Arpan/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_gamma_direct_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_direct_pbe_ar.append(tmp[0])
    zprs_direct_pbe_gw_ar.append(tmp[1])

zprs_direct_pbe_ar = np.array(zprs_direct_pbe_ar) - zprs_direct_pbe_ar[0]
zprs_direct_pbe_gw_ar = np.array(zprs_direct_pbe_gw_ar) - zprs_direct_pbe_gw_ar[0]

print(zprs_direct_pbe_ar)
print(zprs_direct_pbe_gw_ar)

T_pbe = [0,100,200,300,400,500,600,700]
zprs_indirect_pbe_ar = []
zprs_indirect_pbe_gw_ar = []
for t in T_lda:
    prefix = "./60Ry-PBE-Arpan/c.welph.save.pdep200.T%d"%(t)
    tmp = extract_indirect_zpr(prefix,vbm=4,cbm=5,enable_gw=True)
    zprs_indirect_pbe_ar.append(tmp[0])
    zprs_indirect_pbe_gw_ar.append(tmp[1])

zprs_indirect_pbe_ar = np.array(zprs_indirect_pbe_ar) - zprs_indirect_pbe_ar[0]
zprs_indirect_pbe_gw_ar = np.array(zprs_indirect_pbe_gw_ar) - zprs_indirect_pbe_gw_ar[0]

print(zprs_indirect_pbe_ar)
print(zprs_indirect_pbe_gw_ar)


# In[10]:


fig = plt.figure(figsize=(8,4.5))


plt.plot(antonius_dfpt["T"],antonius_dfpt["zpr"],"s--",label="Antonius et al., LDA",alpha=0.3)
plt.plot(kresse_dft["T"],kresse_dft["zpr"],"s--",label="Karsai et al., PBE",alpha=0.3)
plt.plot(monserrat_dfpt["T"],monserrat_dfpt["zpr"],"s--",label="Monserrat, LDA",alpha=0.3)

plt.plot(gapA1["T"],gapA1["gap"],"v",c='k',label="Expt1",alpha=0.3)
plt.plot(gapA2["T"],gapA2["gap"],"^",c='k',label="Expt2",alpha=0.3)
# plt.plot(T_lda,zprs_direct_lda_gw,"o-",label="This work, ZPR@GW@LDA")


plt.plot(T_lda,zprs_direct_lda,"o-",c="C3",label="This work, LDA")
# plt.plot(T_pbe,zprs_direct_pbe_kr,"o-",label="This work, PBE, Karsai lattice")
# plt.plot(T_pbe,zprs_direct_pbe_ar,"o-",label="This work, PBE, Kundu lattice")
plt.plot(T_pbe,zprs_direct_pbe_rlx,"o-",c="C4",label="This work, PBE")

plt.legend(fontsize=10,loc="lower left")
plt.xlim([0,750])
plt.ylim([-100,5])
plt.xlabel("Temperature [Kelvin]",fontsize=13)
plt.ylabel("Direct gap renormalization [meV]",fontsize=13)
plt.show()
fig.savefig("Diamond_temperature_dependence_direct.png",dpi=200,bbox_inches="tight")


# In[11]:


# fig = plt.figure(figsize=(8,4.5))
# plt.plot(T_lda,zprs_direct_lda,"o-",label="This work, LDA, Antonius lattice")
# # plt.plot(T_pbe,zprs_direct_pbe_kr,"o-",label="This work, PBE, Karsai lattice")
# # plt.plot(T_pbe,zprs_direct_pbe_ar,"o-",label="This work, PBE, Kundu lattice")
# plt.plot(T_pbe,zprs_direct_pbe_rlx,"o-",label="This work, PBE, Relaxed lattice")


# # plt.plot(antonius_dfpt["T"],antonius_dfpt["zpr"],"s--",label="Antonius et al., LDA")
# # plt.plot(kresse_dft["T"],kresse_dft["zpr"],"s--",label="Karsai et al., PBE")
# # plt.plot(monserrat_dfpt["T"],monserrat_dfpt["zpr"],"s--",label="Monserrat, LDA")

# plt.plot(gapA1["T"],gapA1["gap"],"v",c='k')
# plt.plot(gapA2["T"],gapA2["gap"],"^",c='k')
# # plt.plot(T_lda,zprs_direct_lda_gw,"o-",label="This work, ZPR@GW@LDA")
# plt.legend(fontsize=13,loc="lower left")
# plt.xlim([0,750])
# plt.ylim([-100,5])
# plt.xlabel("Temperature [Kelvin]",fontsize=13)
# plt.ylabel("Direct gap renormalization [meV]",fontsize=13)
# plt.show()

# fig.savefig("Diamond_temperature_dependence_direct.png",dpi=200,bbox_inches="tight")


# In[14]:


# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# fig = plt.figure(figsize=(8,4.5))
# ax = plt.gca()
# plt.plot(T_lda,zprs_indirect_lda,"o-",label="This work, LDA",c="C0")
# plt.plot(T_pbe,zprs_indirect_pbe_rlx,"o-",label="This work, PBE",c="C1")

# plt.plot(arpan_fp_128["T"],arpan_fp_128["center"],"-",label="Fronzen Phonon, PBE",c="C2")

# plt.plot(kresse_dft_indirect["T"],kresse_dft_indirect["gap"],"s--",label="Karsai et al., PBE",c="C3")
# plt.legend(fontsize=10,loc="upper right")
# plt.plot(chen["T"],chen["gap"],"^",c='k')


# plt.xlim([0,750])
# plt.ylim([-100,5])
# plt.xlabel("Temperature [Kelvin]",fontsize=13)
# plt.ylabel("Indirect gap renormalization [meV]",fontsize=13)

# # axin = inset_axes(ax,  width="65%", height="65%",loc=3,bbox_to_anchor=(.075, .1, .75, .75),bbox_transform=ax.transAxes,)
# # axin.plot(T_pbe,zprs_indirect_pbe_rlx,"o-",label="Relaxed lattice",c="C1")
# # axin.plot(T_pbe,zprs_indirect_pbe_kr,"o-",label="Karsai lattice",c="C4")
# # axin.plot(T_pbe,zprs_indirect_pbe_ar,"o-",label="Kundu lattice",c="C5")
# # plt.plot(arpan_fp_128["T"],arpan_fp_128["center"],"-",label="Fronzen Phonon",c="C2")
# # plt.xlim([500,700])
# # plt.ylim([-100,-25])
# # plt.legend(loc="lower left",fontsize=9)
# plt.show()
# fig.savefig("Diamond_temperature_dependence_indirect.png",dpi=200,bbox_inches="tight")


# In[13]:


fig = plt.figure(figsize=(8,4.5))

# plt.plot(T_lda,zprs_indirect_lda_gw,"o-",label="This work, ZPR@GW@LDA")
plt.plot(arpan_fp_128["T"],arpan_fp_128["center"],"-",label="Fronzen Phonon, PBE",alpha=0.3)

plt.plot(kresse_dft_indirect["T"],kresse_dft_indirect["gap"],"s--",label="Karsai et al., PBE",alpha=0.3)
plt.plot(chen["T"],chen["gap"],"p",c='k',label="Expt3",alpha=0.3)

plt.plot(T_lda,zprs_indirect_lda,"o-",c="C3",label="This work, LDA")
# plt.plot(T_pbe,zprs_indirect_pbe_kr,"o-",label="This work, PBE, Karsai lattice")
# plt.plot(T_pbe,zprs_indirect_pbe_ar,"o-",label="This work, PBE, Kundu lattice")
plt.plot(T_pbe,zprs_indirect_pbe_rlx,"o-",c="C4",label="This work, PBE")

plt.legend(fontsize=13,loc="lower left")
plt.xlim([0,750])
plt.ylim([-100,5])
plt.xlabel("Temperature [Kelvin]",fontsize=13)
plt.ylabel("Indirect gap renormalization [meV]",fontsize=13)
plt.show()
fig.savefig("Diamond_temperature_dependence_indirect.png",dpi=200,bbox_inches="tight")


