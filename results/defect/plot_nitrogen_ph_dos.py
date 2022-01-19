#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def ph_dos(phonons,sigma=0.05,normalized=True):
    minfreq = min(phonons)
    maxfreq = max(phonons)
    freq_range = np.arange(minfreq-0.5,maxfreq+0.5,0.02)
    dos = np.zeros_like(freq_range)
    for i, freq in enumerate(freq_range):
        for ph in phonons:
            dos[i] += gaussian(freq,ph,sigma)
    if normalized:
        dos = dos / np.max(dos)
    return freq_range, dos

# phonons3 = pd.read_csv("./two-B-in-3x3x3-50Ry/b.welph.save.pdep800/phonon_iq00001.csv",sep="\\s+",names=["imode","au","thz","cmm"],skiprows=1)
phonons4 = pd.read_csv("./two-B-in-4x4x4-50Ry/b.welph.save.pdep1000/phonon_iq00001.csv",sep="\\s+",names=["imode","au","thz","cmm"],skiprows=1)
phonons5 = pd.read_csv("./two-B-in-5x5x5-50Ry/b.welph.save.pdep1200/phonon_iq00001.csv",sep="\\s+",names=["imode","au","thz","cmm"],skiprows=1)
# freq_range3, dos3 = ph_dos(phonons3["thz"],sigma=0.05)
freq_range4, dos4 = ph_dos(phonons4["thz"],sigma=0.1)
freq_range5, dos5 = ph_dos(phonons5["thz"],sigma=0.1)

fig = plt.figure(figsize=(8,4.5))
# plt.plot(freq_range3,dos3,label="3x3x3")
plt.plot(freq_range4,dos4,label="4x4x4")
plt.plot(freq_range5,dos5,label="5x5x5")
plt.legend()
plt.xlabel("Phonon frequencies [THz]")
plt.ylabel("Phonon density of states")
fig.savefig("boron-ph-dos.png",bbox_inches="tight",dpi=300)
