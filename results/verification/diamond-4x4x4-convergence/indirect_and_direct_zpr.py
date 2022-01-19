#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_ZPR(prefix,vbmskipline=4,cbmskipline=29,enable_gw=False):
    zprs = np.zeros([2])
    fmfname = prefix +"/reFMselfen_DFT_adi.tab"
    vbm_fm = 0
    cbm_fm = 0
    with open(fmfname,"r") as f:
        for i in range(vbmskipline):
            f.readline()
        line = f.readline()
        vbm_fm = float(line.split()[3])
    with open(fmfname,"r") as f:
        for i in range(cbmskipline):
            f.readline()
        line = f.readline()
        cbm_fm = float(line.split()[3])
    dwfname = prefix + "/reDWselfen_DFT.tab"
    vbm_dw = 0
    cbm_dw = 0
    with open(dwfname,"r") as f:
        for i in range(vbmskipline):
            f.readline()
        line = f.readline()
        vbm_dw = float(line.split()[3])
    with open(dwfname,"r") as f:
        for i in range(cbmskipline):
            f.readline()
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
            for i in range(vbmskipline):
                f.readline()
            line = f.readline()
            vbm_fm = float(line.split()[3])
        with open(fmfname,"r") as f:
            for i in range(cbmskipline):
                f.readline()
            line = f.readline()
            cbm_fm = float(line.split()[3])
        dwfname = prefix + "/reDWselfen_eqpgw.tab"
        vbm_dw = 0
        cbm_dw = 0
        with open(dwfname,"r") as f:
            for i in range(vbmskipline):
                f.readline()
            line = f.readline()
            vbm_dw = float(line.split()[3])
        with open(dwfname,"r") as f:
            for i in range(cbmskipline):
                f.readline()
            line = f.readline()
            cbm_dw = float(line.split()[3])
        vbm_zpr = vbm_fm + vbm_dw
        cbm_zpr = cbm_fm + cbm_dw

        zprs[1] = cbm_zpr - vbm_zpr
    return np.array(zprs)

df = pd.read_csv("./ref-data/2018-Kresse-NJP-fig6-5x5x5-PBE.csv")
df["zpr"] = ( df["zpr"] - df["zpr"].values[0] ) * 1000
T_pbe_ref = df["T"].values
zprs_pbe_ref = df["zpr"].values

T_pbe = [0,100,200,300,400,500,600,700]
zprs_pbe4_relax_indirect = []
# zprs_pbe4_gw_relax = []
for t in T_pbe:
    prefix = "./60Ry-PBE-myrelax/c.welph.save.pdep200.T%d"%(t)
    tmp = read_ZPR(prefix,vbmskipline=4,cbmskipline=29,enable_gw=True)
    zprs_pbe4_relax_indirect.append(tmp[0])
    # zprs_pbe4_gw_relax.append(tmp[1])
zprs_pbe4_relax_indirect = np.array(zprs_pbe4_relax_indirect) - zprs_pbe4_relax_indirect[0]
# zprs_pbe4_gw_relax = np.array(zprs_pbe4_gw_relax) - zprs_pbe4_gw_relax[0]

T_pbe = [0,100,200,300,400,500,600,700]
zprs_pbe4_relax_direct = []
# zprs_pbe4_gw_relax = []
for t in T_pbe:
    prefix = "./60Ry-PBE-myrelax/c.welph.save.pdep200.T%d"%(t)
    tmp = read_ZPR(prefix,vbmskipline=4,cbmskipline=5,enable_gw=True)
    zprs_pbe4_relax_direct.append(tmp[0])
    # zprs_pbe4_gw_relax.append(tmp[1])
zprs_pbe4_relax_direct = np.array(zprs_pbe4_relax_direct) - zprs_pbe4_relax_direct[0]
# zprs_pbe4_gw_relax = np.array(zprs_pbe4_gw_relax) - zprs_pbe4_gw_relax[0]


fig = plt.figure(figsize=(8,4.5))
# plt.plot(T_pbe_ref,zprs_pbe_ref,"x-",label="Kresse PBE 5x5x5")
plt.plot(T_pbe,zprs_pbe4_relax_direct,"o-",label="This work, PBE 4x4x4, relaxed lattice, direct")
plt.plot(T_pbe,zprs_pbe4_relax_indirect,"o-",label="This work, PBE 4x4x4, relaxed lattice, indirect")
# plt.plot(T_pbe,zprs_pbe4_kr,"o-",label="This work, PBE 4x4x4, Kresse lattice")
# plt.plot(T_pbe,zprs_pbe5_kr,"o-",label="This work, PBE 5x5x5, Kresse lattice")
plt.legend(fontsize=11,loc="lower left")
plt.xlabel("Temperature [Kelvin]",fontsize=13)
plt.ylabel("Indirect gap renormalization [meV]",fontsize=13)
fig.savefig("Compare_direct_and_indirect.png",dpi=200,bbox_inches="tight")






