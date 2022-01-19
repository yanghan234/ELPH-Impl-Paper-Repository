#!/usr/bin/env python
import numpy as np
import pandas as pd

def extract_zpr(prefix,vbm,cbm,enable_gw=False,adiabatic=True):
    zpr_dft = 0
    zpr_gw  = 0
    if adiabatic:
        fmfname = prefix +"/reFMselfen_DFT_adi.tab"
    else:
        fmfname = prefix +"/reFMselfen_DFT_nad.tab"
    dwfname = prefix +"/reDWselfen_DFT.tab"
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

prefix = "./60Ry/c.welph.save.pdep200/"
zpr_dft_adi, zpr_gw_adi = extract_zpr(prefix,vbm=4,cbm=5,enable_gw=True,adiabatic=True)
zpr_dft_nad, zpr_gw_nad = extract_zpr(prefix,vbm=4,cbm=5,enable_gw=True,adiabatic=False)
print("Adiabatic Gap ZPR@DFT = %8.4f"%(zpr_dft_adi))
print("Adiabatic Gap ZPR@GW = %8.4f"%(zpr_gw_adi))
print("Non-adiabatic Gap ZPR@DFT = %8.4f"%(zpr_dft_nad))
print("Non-adiabatic Gap ZPR@GW = %8.4f"%(zpr_gw_nad))

