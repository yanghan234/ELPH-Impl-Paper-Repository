#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pristine-diamond.csv")
df.replace("nan",np.nan)
df["adigw"] = df["adigw"].astype(float)
df["nadgw"] = df["nadgw"].astype(float)
print(df)

def linear_fit(x,y):
    coeff = np.polyfit(x,y,1)
    return np.poly1d(coeff)


adipbefit = linear_fit(df["invN3"],df["adipbe"])
adipbefit_test = linear_fit(df[df["N"]<=5]["invN3"],df[df["N"]<=5]["adipbe"])
adigwfit = linear_fit(df[df["N"]<=5]["invN3"],df[df["N"]<=5]["adigw"])
nadpbefit = linear_fit(df["invN3"],df["nadpbe"])
nadpbefit_test = linear_fit(df[df["N"]<=5]["invN3"],df[df["N"]<=5]["nadpbe"])
nadgwfit = linear_fit(df[df["N"]<=5]["invN3"],df[df["N"]<=5]["nadgw"])
print(f"Interpolated     adibatic ZPR@PBE (fitted to 10) = {adipbefit(0):6.2f}")
print(f"Interpolated non-adibatic ZPR@PBE (fitted to 10) = {nadpbefit(0):6.2f}")
print(f"Interpolated     adibatic ZPR@PBE (fitted to 5) = {adipbefit_test(0):6.2f}")
print(f"Interpolated non-adibatic ZPR@PBE (fitted to 5) = {nadpbefit_test(0):6.2f}")
#print( "Interpolated     adibatic ZPR@PBE, rigid shifted = %6.2f"%(adipbefit(0)-df["adipbe"].values[2]+df["adipbe"].values[2]))
#print( "Interpolated non-adibatic ZPR@PBE, rigid shifted = %6.2f"%(nadpbefit(0)-df["nadpbe"].values[2]+df["nadpbe"].values[2]))
print(f"adigwfit = {adigwfit.__str__}")
print(f"nadgwfit = {nadgwfit.__str__}")

fig = plt.figure(figsize=(9,4.5))
plt.plot(df["invN3"],df["adipbe"],"o-",label="Adibatic PBE")
plt.plot(df["invN3"],adipbefit(df["invN3"]),"--",c="C0",alpha=0.5)
plt.plot(df["invN3"],df["nadpbe"],"^-",label="Non-adiabatic PBE")
plt.plot(df["invN3"],nadpbefit(df["invN3"]),"--",c="C1",alpha=0.5)
# plt.plot(df["invN3"],df["adigw"],"o-",label="Adibatic GW")
# plt.plot(df[df["N"]<=5]["invN3"],adigwfit(df[df["N"]<=5]["invN3"]),"--",c="C2",alpha=0.5)
# plt.plot(df["invN3"],df["nadgw"],"^-",label="Non-adibatic GW")
# plt.plot(df[df["N"]<=5]["invN3"],nadgwfit(df[df["N"]<=5]["invN3"]),"--",c="C3",alpha=0.5)
plt.xlabel(r"$1/N_q^3$")
plt.ylabel("ZPR of indirect gap of diamond [meV]")
plt.legend()
plt.show()
fig.savefig("interpolate_indirect_gap_diamond.png",dpi=300,bbox_inches="tight")
