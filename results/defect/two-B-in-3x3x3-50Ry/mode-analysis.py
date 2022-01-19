#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mode = pd.read_csv("./mode-160.csv",names=["index","x","y","z","sqsum"])
nearest_to_1 = [6,14,38]
nearest_to_2 = [3,7,19]

print(mode["index"].isin(nearest_to_1))


fig = plt.figure(figsize=(8,4.5))
plt.plot(mode["index"],mode["sqsum"],"o",label="All")
plt.plot(mode[mode["index"].isin(nearest_to_1)]["index"],
         mode[mode["index"].isin(nearest_to_1)]["sqsum"],"^",label="Nearest to B1")
plt.plot(mode[mode["index"].isin(nearest_to_2)]["index"],
         mode[mode["index"].isin(nearest_to_2)]["sqsum"],"v",label="Nearest to B2")
plt.axhline(mode["sqsum"].mean(),c="k",label="Average")
plt.legend()
plt.xlabel("Index of atom")
plt.ylabel("Contribution of each atom")
fig.savefig("mode-160.png",dpi=300,bbox_inches="tight")
plt.show()


