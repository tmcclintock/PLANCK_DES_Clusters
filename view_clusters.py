import numpy as np
import matplotlib.pyplot as plt
plt.rc("text", usetex=True)
#plt.rc("font", size=14)

deltasigma = np.loadtxt("data/dsig_data.txt")
err  = np.loadtxt("data/error_bars.txt")

N_clusters = len(err)
N_bins = len(err[0])

Redges = np.logspace(np.log10(0.0323), np.log10(30.), num=N_bins+1)
Rmid = (Redges[:-1] + Redges[1:])/2. #midpoint

Nx = 3
Ny = 3
fig, axarr = plt.subplots(Nx, Ny, sharex=True)
for i in range(Nx):
    for j in range(Ny):
        index = j*Nx + i
        axarr[i][j].errorbar(Rmid, deltasigma[index], err[index], ls='', marker='.')
        axarr[i][j].set_yscale('log')
        axarr[i][j].set_xscale('log')
plt.subplots_adjust(wspace=0.25)
plt.show()
