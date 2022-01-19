#!/usr/bin/env python
# coding: utf-8

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


# Kresse
kresse_dft = pd.read_csv("../ref-data/2018-Kresse-NJP-fig5-4x4x4-DFT.csv")
kresse_gw = pd.read_csv("../ref-data/2018-Kresse-NJP-fig5-4x4x4-GW.csv")

# Antonius 2014
antonius_dfpt = pd.read_csv("../ref-data/2014-Antonius-PRL-fig3-DFPT.csv")
antonius_dfpt["zpr"] = ( antonius_dfpt["gap"] - antonius_dfpt["gap"].values[0] ).values * 1000

antonius_dfpt_gw = pd.read_csv("../ref-data/2014-Antonius-PRL-fig3-DFPT+GW.csv")
antonius_dfpt_gw["zpr"] = ( antonius_dfpt_gw["gap"] - antonius_dfpt_gw["gap"].values[0] ).values * 1000

# Bartomeu Monserrat, PHYSICAL REVIEW B 93, 100301(R) (2016)
monserrat_dft = pd.read_csv("../ref-data/2016-Monserrat-PRB-DFPT.csv")
monserrat_gw = pd.read_csv("../ref-data/2016-Monserrat-PRB-DFPT+GW.csv")

monserrat_dft["zpr"] = ( monserrat_dft["zpr"] - monserrat_dft["zpr"].values[0]).values
monserrat_gw["zpr"]  = ( monserrat_gw["zpr"] - monserrat_gw["zpr"].values[0]).values

# Experimental direct gap extracted from
# S. Logothetidis, J. Petalas, H. M. Polatoglou, and D. Fuchs
# Phys. Rev. B 46, 4483
gapA1 = pd.read_csv("../ref-data/gapA1.csv")
gapA2 = pd.read_csv("../ref-data/gapA2.csv")
gapB1 = pd.read_csv("../ref-data/gapB1.csv")
gapB2 = pd.read_csv("../ref-data/gapB2.csv")
fitted = pd.read_csv("../ref-data/fitted.csv")
errorbar = pd.read_csv("../ref-data/errorbar.csv")


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

# monserrat_dfpt


# In[190]:


def read_ZPR(prefix,skipline=4,enable_gw=False):
    zprs = np.zeros([2])
    fmfname = prefix +"/reFMselfen_DFT_adi.tab"
    vbm_fm = 0
    cbm_fm = 0
    with open(fmfname,"r") as f:
        for i in range(skipline):
            f.readline()
        line = f.readline()
        vbm_fm = float(line.split()[3])
        line = f.readline()
        cbm_fm = float(line.split()[3])
    dwfname = prefix + "/reDWselfen_DFT.tab"
    vbm_dw = 0
    cbm_dw = 0
    with open(dwfname,"r") as f:
        for i in range(skipline):
            f.readline()
        line = f.readline()
        vbm_dw = float(line.split()[3])
        line = f.readline()
        cbm_dw = float(line.split()[3])
    
    vbm_zpr = vbm_fm + vbm_dw
    cbm_zpr = cbm_fm + cbm_dw
    zprs[0] = cbm_zpr - vbm_zpr
    
    if enable_gw:
        fmfname = prefix +"/reFMselfen_eqpgw_adi.tab"
        vbm_fm = 0
        cbm_fm = 0
        with open(fmfname,"r") as f:
            for i in range(skipline):
                f.readline()
            line = f.readline()
            vbm_fm = float(line.split()[3])
            line = f.readline()
            cbm_fm = float(line.split()[3])
        dwfname = prefix + "/reDWselfen_eqpgw.tab"
        vbm_dw = 0
        cbm_dw = 0
        with open(dwfname,"r") as f:
            for i in range(skipline):
                f.readline()
            line = f.readline()
            vbm_dw = float(line.split()[3])
            line = f.readline()
            cbm_dw = float(line.split()[3])
        vbm_zpr = vbm_fm + vbm_dw
        cbm_zpr = cbm_fm + cbm_dw
        zprs[1] = cbm_zpr - vbm_zpr
    return np.array(zprs)


T_lda = [0,100,200,300,400,500,600,700]
zprs_lda60 = []
# zprs_lda_gw = []
for t in T_lda:
    prefix = "../60Ry/c.welph.save.pdep200.T%d"%(t)
    tmp = read_ZPR(prefix,skipline=4,enable_gw=False)
    zprs_lda60.append(tmp[0])
    # zprs_lda_gw.append(tmp[1])
zprs_lda60 = np.array(zprs_lda60) - zprs_lda60[0]
# zprs_lda_gw = np.array(zprs_lda_gw) - zprs_lda_gw[0]

zprs_lda80 = []
for t in T_lda:
    prefix = "./c.welph.save.pdep200.T%d"%(t)
    tmp = read_ZPR(prefix,skipline=4,enable_gw=False)
    zprs_lda80.append(tmp[0])
zprs_lda80 = np.array(zprs_lda80) - zprs_lda80[0]
#
# fig = plt.figure(figsize=(8,4.5))
# plt.plot(kresse_dft["T"],kresse_dft["zpr"],"x-", label="Karsai et al., LDA")
# plt.plot(kresse_gw["T"], kresse_gw["zpr"], "x--",label="Karsai et al., LDA+GW")
# plt.plot(antonius_dfpt["T"],antonius_dfpt["zpr"],"s-",label="Antonius et al., LDA")
# plt.plot(antonius_dfpt_gw["T"],antonius_dfpt_gw["zpr"],"s--",label="Antonius et al., LDA+GW")
# plt.plot(monserrat_dft["T"],monserrat_dft["zpr"],"d-",label="Monserrat, LDA")
# plt.plot(monserrat_gw["T"],monserrat_gw["zpr"],"d--",label="Monserrat, LDA+GW")
# plt.plot(T_lda,zprs_lda,"o-",label="This work, LDA")
# plt.plot(T_lda,zprs_lda_gw,"o--",label="This work, LDA+GW")
# plt.plot(T_pbe,zprs_pbe,"o-",label="This work, PBE")
# plt.plot(T_pbe_te,zprs_pbe_te,"o-",label="This work, PBE+TE")
# plt.plot(T_pbe_te,zprs_pbe_gw_te,"o--",label="This work, PBE+GW+TE")
# plt.plot(gapA1["T"],gapA1["gap"],'^',c='k',label="Type IIa method 1")
# plt.plot(gapA2["T"],gapA2["gap"],'v',c='k',label="Type IIa method 2")
# plt.legend(fontsize=11,loc="lower left")
# plt.xlabel("Temperature [Kelvin]",fontsize=13)
# plt.ylabel("Direct gap renormalization [meV]",fontsize=13)
# plt.show()
# fig.savefig("Diamond_temperature_dependence.png",dpi=200,bbox_inches="tight")

## DFT ONLY
fig = plt.figure(figsize=(8,4.5))
plt.plot(kresse_dft["T"],kresse_dft["zpr"],"x-", label="Karsai et al., LDA")
plt.plot(antonius_dfpt["T"],antonius_dfpt["zpr"],"s-",label="Antonius et al., LDA")
plt.plot(monserrat_dft["T"],monserrat_dft["zpr"],"d-",label="Monserrat, LDA")
plt.plot(T_lda,zprs_lda60,"o-",label="This work, LDA (Antonius lattice), 60 Ry")
plt.plot(T_lda,zprs_lda80,"o-",label="This work, LDA (Antonius lattice), 80 Ry")
# plt.plot(T_lda,zprs_lda_relax,"o-",label="This work, LDA (relaxed lattice)")
# plt.plot(T_pbe,zprs_pbe_relax,"o-",label="This work, PBE (relaxed lattice)")
# plt.plot(T_pbe,zprs_pbe_kr,"o-",label="This work, PBE (Kresse lattice)")
# plt.plot(T_pbe,zprs_pbe,"o-",label="This work, PBE (Arpan lattice@100K) ")
# plt.plot(T_pbe_te,zprs_pbe_te,"o-",label="This work, PBE+TE (Arpan lattice)")
plt.plot(gapA1["T"],gapA1["gap"],'^',c='k',label="Type IIa method 1")
plt.plot(gapA2["T"],gapA2["gap"],'v',c='k',label="Type IIa method 2")
plt.legend(fontsize=11,loc="lower left")
plt.xlabel("Temperature [Kelvin]",fontsize=13)
plt.ylabel("Direct gap renormalization [meV]",fontsize=13)
plt.show()
fig.savefig("Diamond_temperature_dependence_DFT.png",dpi=200,bbox_inches="tight")

