"""
Make a histogram of the masses.
"""
import matplotlib.pyplot as plt
plt.rc("text", usetex=True)
import numpy as np
h=0.7

def get_mass_array():
    zs = np.loadtxt("data/z.txt")
    lMs = []
    for i in range(len(zs)):
        lMs.append(np.loadtxt("results/bestfits/bf_cluster%d.txt"%i)[0])
    return np.array(lMs).flatten()

if __name__ == "__main__":
    #lMs = get_mass_array()
    #np.savetxt("results/l10masses.txt", lMs)
    lMs = np.loadtxt("results/l10masses.txt")
    lMs -= np.log10(h) #Msun from Msun/h
    plt.hist(lMs, 50, facecolor="gray", alpha=0.7)
    plt.xlabel(r"$\log_{10}M\ [{\rm M_\odot}]$")
    plt.ylabel(r"${\rm Number}$")
    plt.show()
