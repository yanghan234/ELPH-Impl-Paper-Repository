#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fm_adi = pd.read_csv("./b.welph.save.pdep800/reFMselfen_DFT_adi_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")

fm_nad = pd.read_csv("./b.welph.save.pdep800/reFMselfen_DFT_nad_resolved.tab",
            names=["iks","ibn","iq","imode","en","fm"],skiprows=1,
            sep="\\s+")

print(fm_adi[fm_adi["ibn"]==108].sum())
print(fm_nad[fm_nad["ibn"]==108].sum())

plt.plot(range(fm_adi[fm_adi["ibn"]==108].shape[0]),fm_adi[fm_adi["ibn"]==108]["fm"],label="adiabatic")
plt.plot(range(fm_nad[fm_nad["ibn"]==108].shape[0]),fm_nad[fm_nad["ibn"]==108]["fm"],label="non-adiabatic")
plt.legend()
plt.show()
