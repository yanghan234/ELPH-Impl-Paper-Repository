#!/usr/bin/env python
import numpy as np
import pandas as pd

def extract_zpr(prefix,vbm,cbm,enable_gw=False):
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

prefix = "./c.welph.save.pdep200"
zpr_pbe, zpr_gw = extract_zpr(prefix,vbm=4,cbm=5,enable_gw=False)
print(zpr_pbe)
print(zpr_gw)

