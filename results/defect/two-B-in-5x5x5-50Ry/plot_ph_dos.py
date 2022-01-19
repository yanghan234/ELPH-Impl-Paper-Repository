#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def ph_dos(phonons,sigma=0.05):
    minfreq = min(phonons)
    maxfreq = max(phonons)
    freq_range = np.arange(minfreq-0.5,maxfreq+0.5,0.02)
    dos = np.zeros_like(freq_range)
    for i, freq in enumerate(freq_range):
        for ph in phonons:
            dos[i] += gaussian(freq,ph,sigma)
    return freq_range, dos

phonons = pd.read_csv("./b.welph.save.pdep1200/phonon_iq00001.csv",sep="\\s+",names=["imode","au","thz","cmm"],skiprows=1)
freq_range, dos = ph_dos(phonons["thz"],sigma=0.05)

# print(phonons.head())
# print(phonons["thz"].values)

fig = plt.figure(figsize=(8,4.5))
plt.plot(freq_range,dos)
# for ph in phonons["thz"]:
#     plt.axvline(ph,ymin=0,ymax=1)
#plt.show()
fig.savefig("dos-5x5x5.png",bbox_inches="tight",dpi=300)
