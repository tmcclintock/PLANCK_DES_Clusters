import numpy as np
import matplotlib.pyplot as plt
plt.rc("text", usetex=True)
#plt.rc("font", size=14)
import helper_functions as HF

deltasigma, err = HF.get_all_data()

N_clusters = len(err)
N_bins = len(err[0])

Redges, Rmid = HF.get_Redges_and_Rmid(N_bins)

Nx = 3
Ny = 3
fig, axarr = plt.subplots(Nx, Ny, sharex=True)
for i in range(Nx):
    for j in range(Ny):
        index = j*Nx + i
        Rinds, DS, DSerr = HF.fix_data(Rmid, deltasigma[index], err[index])
        axarr[i][j].errorbar(Rinds, DS, DSerr, ls='', marker='.')
        axarr[i][j].set_yscale('log')
        axarr[i][j].set_xscale('log')
plt.subplots_adjust(wspace=0.25)
plt.show()
