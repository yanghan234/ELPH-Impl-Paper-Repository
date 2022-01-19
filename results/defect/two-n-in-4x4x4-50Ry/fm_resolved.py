#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

phonons = pd.read_csv("./n2.welph.save.pdep1000/phonon_iq00001.csv",sep="\\s+",names=["imode","au","thz","cmm"],skiprows=1)

fm_adi = pd.read_csv("./n2.welph.save.pdep1000/reFMselfen_DFT_adi_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")

defect_fm_adi = fm_adi[fm_adi["ibn"]==257]["fm"].values

fm_nad = pd.read_csv("./n2.welph.save.pdep1000/reFMselfen_DFT_nad_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")
defect_fm_nad = fm_nad[fm_nad["ibn"]==257]["fm"].values


fm_diff = []
for i in range(len(defect_fm_adi)):
    fm_diff.append((i+1,defect_fm_adi[i],defect_fm_nad[i],defect_fm_nad[i]-defect_fm_adi[i]))

print("Total difference = %6.2f"%np.sum([x[3] for x in fm_diff]))

fm_diff = sorted(fm_diff,key=lambda tup: -tup[3])
print(fm_diff[:10])

# plt.plot(range(fm_adi[fm_adi["ibn"]==257].shape[0]),fm_adi[fm_adi["ibn"]==257]["fm"],"o",label="adiabatic")
# plt.plot(range(fm_nad[fm_nad["ibn"]==257].shape[0]),fm_nad[fm_nad["ibn"]==257]["fm"],"o",label="non-adiabatic")
fig = plt.figure(figsize=(8,4.5))
# plt.plot(range(fm_nad[fm_nad["ibn"]==257].shape[0]),fm_nad[fm_nad["ibn"]==257]["fm"]-fm_adi[fm_adi["ibn"]==257]["fm"],"o",label="Nonadiabatic-Adiabatic")
plt.plot(phonons["thz"],fm_nad[fm_nad["ibn"]==257]["fm"]-fm_adi[fm_adi["ibn"]==257]["fm"],"o",label="Nonadiabatic-Adiabatic")
plt.grid()
plt.xlabel("Index of phonon mode")
plt.ylabel("Difference in ZPR [meV]")
# plt.legend()
plt.show()
fig.savefig("difference_in_zpr_nitrogen4.png",dpi=300,bbox_inches="tight")
