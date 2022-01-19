#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_all_modes(fname,natoms):
    def extract_line(line):
        line = line.strip()[1:-1]
        floats = [float(x) for x in line.split()]
        return np.complex(floats[0],floats[1]),\
               np.complex(floats[2],floats[3]),\
               np.complex(floats[4],floats[5])

    modes = np.zeros([natoms*3,natoms*3],dtype=complex)
    with open(fname,"r") as f:
        all_lines = f.readlines()
        line_ind = 0
        while "freq" not in all_lines[line_ind]:
            line_ind += 1

        imode = 0
        while imode < natoms * 3:
            ind = 0
            lines = all_lines[line_ind+1:line_ind+natoms+1]
            for line in lines:
                modes[imode][ind],modes[imode][ind+1],modes[imode][ind+2] = extract_line(line)
                ind += 3
            imode += 1
            line_ind += natoms+1
    return modes

## get all modes and get the fraction of boron atoms
natoms = 4*4*4*2
total_modes = natoms*3
fname = "./b.welph.save.pdep1000/dyn1"
modes = read_all_modes(fname,natoms)
defect_frac = np.array([np.absolute(mode[0])+np.absolute(mode[1]) for mode in modes])

homo = 255
defect = 256
lumo = 257
prefix = "b"
npdep = 1000

fm_adi = pd.read_csv(f"./{prefix}.welph.save.pdep{npdep}/reFMselfen_DFT_adi_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")

defect_fm_adi = fm_adi[fm_adi["ibn"]==defect]["fm"].values
gap_fm_adi = fm_adi[fm_adi["ibn"]==lumo]["fm"].values - \
            fm_adi[fm_adi["ibn"]==homo]["fm"].values

fm_nad = pd.read_csv(f"./{prefix}.welph.save.pdep{npdep}/reFMselfen_DFT_nad_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")
defect_fm_nad = fm_nad[fm_nad["ibn"]==defect]["fm"].values
gap_fm_nad = fm_nad[fm_nad["ibn"]==lumo]["fm"].values - \
            fm_nad[fm_nad["ibn"]==homo]["fm"].values

# defect_fm_diff = []
# gap_fm_diff = []
# for i in range(len(defect_fm_adi)):
#     defect_fm_diff.append((i+1,defect_fm_adi[i],defect_fm_nad[i],defect_fm_nad[i]-defect_fm_adi[i]))
#     gap_fm_diff.append((i+1,gap_fm_adi[i],gap_fm_nad[i],gap_fm_nad[i]-gap_fm_adi[i]))
# 
# defect_fm_diff = sorted(defect_fm_diff,key=lambda tup: tup[3])
# gap_fm_diff = sorted(gap_fm_diff,key=lambda tup: tup[3])
# # print(defect_fm_diff[:10])
# print("Total difference = %8.4f in defect ZPR"%(np.sum([x[3] for x in defect_fm_diff])))
# print("Total difference = %8.4f in gap ZPR"%(np.sum([x[3] for x in gap_fm_diff])))

defect_fm_diff = defect_fm_nad-defect_fm_adi
gap_fm_diff = gap_fm_nad-gap_fm_adi
print("Total difference = %8.4f in defect ZPR"%(np.sum(defect_fm_diff)))
print("Total difference = %8.4f in gap ZPR"%(np.sum(gap_fm_diff)))

print("Contribution of defect vibration to total diff of defect ZPR = %8.4f"%np.sum(defect_fm_diff[defect_frac>0.1]))
print("Contribution of defect vibration to total diff of gap ZPR  = %8.4f"%np.sum(gap_fm_diff[defect_frac>0.1]))

fig = plt.figure(figsize=(8,4.5))
# plt.plot(range(1,1+total_modes),[np.absolute(mode[0])+np.absolute(mode[1]) for mode in modes],"o")

plt.plot(defect_frac,defect_fm_diff,"o",label="Defect ZPR")
plt.plot(defect_frac,gap_fm_diff,"o",label="Host Gap ZPR")
plt.xlabel("Fractional contribution of defect vibration to the mode")
plt.ylabel("Mode-resolved difference between\n adiabatic and non-diabatic ZPR [meV]")
plt.grid()
plt.legend()
plt.show()


# mode_dir = "mode-analysis-fig"
# if not os.path.exists(mode_dir):
#     os.mkdir(mode_dir)
# for imode in range(total_modes):
#     print(f"printing imode = {imode+1}")
#     fig = plt.figure(figsize=(8,4.5))
#     plt.plot(range(1,1+natoms*3),np.absolute(modes[imode]),"o")
#     fig.savefig(os.path.join(mode_dir,f"mode-{imode+1}.png"),bbox_inches="tight",dpi=200)