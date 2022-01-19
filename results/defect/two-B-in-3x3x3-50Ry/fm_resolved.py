#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

homo = 107
defect = 108
lumo = 109
prefix = "b"
npdep = 800

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

defect_fm_diff = []
gap_fm_diff = []
for i in range(len(defect_fm_adi)):
    defect_fm_diff.append((i+1,defect_fm_adi[i],defect_fm_nad[i],defect_fm_nad[i]-defect_fm_adi[i]))
    gap_fm_diff.append((i+1,gap_fm_adi[i],gap_fm_nad[i],gap_fm_nad[i]-gap_fm_adi[i]))

defect_fm_diff = sorted(defect_fm_diff,key=lambda tup: tup[3])
gap_fm_diff = sorted(gap_fm_diff,key=lambda tup: tup[3])
# print(defect_fm_diff[:10])
print("Total difference = %8.4f in defect ZPR"%(np.sum([x[3] for x in defect_fm_diff])))
print("Total difference = %8.4f in gap ZPR"%(np.sum([x[3] for x in gap_fm_diff])))

# plt.plot(range(fm_adi[fm_adi["ibn"]==defect].shape[0]),fm_adi[fm_adi["ibn"]==108]["fm"],"o",label="adiabatic")
# plt.plot(range(fm_nad[fm_nad["ibn"]==defect].shape[0]),fm_nad[fm_nad["ibn"]==108]["fm"],"o",label="non-adiabatic")
fig = plt.figure(figsize=(8,4.5))
plt.plot(range(len(defect_fm_diff)),defect_fm_nad-defect_fm_adi,"o",label="Defect state ZPR")
plt.plot(range(len(gap_fm_diff)),gap_fm_nad-gap_fm_adi,"o",label="Gap ZPR")
plt.grid()
plt.xlabel("Index of phonon mode")
plt.ylabel("Difference in ZPR [meV]")
plt.legend()
plt.show()
fig.savefig("difference_in_zpr_boron3.png",dpi=300,bbox_inches="tight")
