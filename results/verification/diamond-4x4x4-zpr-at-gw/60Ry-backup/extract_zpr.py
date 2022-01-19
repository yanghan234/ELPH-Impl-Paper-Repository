#!/bin/env python3
import numpy as np
import pandas as pd

def extract(fmfname,dwfname,ik=1,bands=[4,5]):
    df1 = pd.read_csv(fmfname,sep="\\s+",skiprows=1,names=["ik","ibn","en","re","im"])
    df2 = pd.read_csv(dwfname,sep="\\s+",skiprows=1,names=["ik","ibn","en","re","im"])

    res = df1[df1["ik"]==ik & df1["ibn"].isin(bands)]["re"].values + \
          df2[df2["ik"]==ik & df2["ibn"].isin(bands)]["re"].values

    for ibn,zpr in zip(bands,res):
        print("ibn = %3d, ZPR = %+6.2f"%(ibn,zpr))


if __name__ == "__main__":
    prefix = "./c.welph.save.nbnd8.lan/"
    fmfname = prefix + "reFMselfen_eqpgw_adi.tab"
    dwfname = prefix + "reDWselfen_eqpgw.tab"
    print(prefix)
    extract(fmfname,dwfname)

    prefix = "./c.welph.save.nbnd100.lan.curv/"
    fmfname = prefix + "reFMselfen_eqpgw_adi.tab"
    dwfname = prefix + "reDWselfen_eqpgw.tab"
    print(prefix)
    extract(fmfname,dwfname)

    prefix = "./c.welph.save.nbnd100.lan.nocurv/"
    fmfname = prefix + "reFMselfen_eqpgw_adi.tab"
    dwfname = prefix + "reDWselfen_eqpgw.tab"
    print(prefix)
    extract(fmfname,dwfname)

    prefix = "./c.welph.save.nbnd100.nolan.nocurv/"
    fmfname = prefix + "reFMselfen_eqpgw_adi.tab"
    dwfname = prefix + "reDWselfen_eqpgw.tab"
    print(prefix)
    extract(fmfname,dwfname)

    prefix = "./c.welph.save.nbnd100.abinit.ppm/"
    fmfname = prefix + "reFMselfen_eqpgw_adi.tab"
    dwfname = prefix + "reDWselfen_eqpgw.tab"
    print(prefix)
    extract(fmfname,dwfname)

