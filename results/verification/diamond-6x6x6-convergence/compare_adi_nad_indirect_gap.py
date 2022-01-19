#!/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def extract_zpr(prefix,vbm,cbm,enable_gw=False,adiabatic=True):
    zpr_dft = 0
    zpr_gw  = 0
    if adiabatic:
        fmfname = os.path.join(prefix,"reFMselfen_DFT_adi.tab")
    else:
        fmfname = os.path.join(prefix,"reFMselfen_DFT_nad.tab")
    dwfname = os.path.join(prefix,"reDWselfen_DFT.tab")
    print(fmfname)
    print(dwfname)
    fm_dft = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    dw_dft = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
    vbm_zpr_dft = fm_dft[fm_dft["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0] + dw_dft[dw_dft["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0]
    cbm_zpr_dft = fm_dft[fm_dft["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0] + dw_dft[dw_dft["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0]
    zpr_dft = cbm_zpr_dft - vbm_zpr_dft

    if ( enable_gw ):
        if adiabatic:
            fmfname = prefix +"/reFMselfen_eqpgw_adi.tab"
        else:
            fmfname = prefix +"/reFMselfen_eqpgw_nad.tab"
        dwfname = prefix +"/reDWselfen_eqpgw.tab"
        fm_gw = pd.read_csv(fmfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        dw_gw = pd.read_csv(dwfname,skiprows=1,sep="\\s+",names=["iks","ibn","en","re","im"])
        vbm_zpr_gw = fm_gw[fm_gw["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0] + dw_gw[dw_gw["ibn"]==vbm].sort_values(by="en").tail(1)["re"].values[0]
        cbm_zpr_gw = fm_gw[fm_gw["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0] + dw_gw[dw_gw["ibn"]==cbm].sort_values(by="en").head(1)["re"].values[0]
        zpr_gw = cbm_zpr_gw - vbm_zpr_gw
    return zpr_dft, zpr_gw

prefix = "./60Ry-Ponce-latt"
prefix = "./60Ry-myrelax"
zprs_adi = []
zprs_nad = []
folder = os.path.join(prefix,f"c.welph.save.pdep200")
zpr_adi, _ = extract_zpr(folder,vbm=4,cbm=5,enable_gw=False,adiabatic=True)
zpr_nad, _ = extract_zpr(folder,vbm=4,cbm=5,enable_gw=False,adiabatic=False)
zprs_adi.append(zpr_adi)
zprs_nad.append(zpr_nad)

print("zpr_adi,zpr_nad")
for zpr_adi, zpr_nad in zip(zprs_adi,zprs_nad):
    print(f"{zpr_adi:.04f},{zpr_nad:.04f}")

zprs_adi = np.array(zprs_adi)
zprs_nad = np.array(zprs_nad)

