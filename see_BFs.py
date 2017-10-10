import numpy as np
import matplotlib.pyplot as plt
plt.rc("text", usetex=True)
#plt.rc("font", size=14)
from helper_functions import *
import clusterwl

deltasigma, err = get_all_data()
zs = np.loadtxt("data/z.txt")
cosmo = get_cosmo()
h = cosmo['h'] #Hubble constant

N_clusters = len(err)
N_bins = len(err[0])

Redges_Mpc, Rmid = get_Redges_and_Rmid(N_bins)

xlabels = [0.1, 1.0, 10.]

Nx = 3
Ny = 3
fig, axarr = plt.subplots(Nx, Ny, sharex=True)
for i in range(Nx):
    for j in range(Ny):
        index = j*Nx + i
        z = zs[index]
        Redges = Redges_Mpc*h*(1+z)
        gud = get_good_indices(Rmid, deltasigma[index])
        bad = get_bad_indices(Rmid, deltasigma[index])
        Rinds, DS, DSerr = Rmid[gud], deltasigma[index, gud], err[index, gud]
        Rbad, DSbad, DSerrbad = Rmid[bad], deltasigma[index, bad], err[index, bad]
        #Rinds, DS, DSerr = fix_data(Rmid, deltasigma[index], err[index])

        k, Plin, Pnl = get_power_spectra(index)
        Rmodel = np.logspace(-2, 3, num=1000, base=10) 
        xi_mm = clusterwl.xi.xi_mm_at_R(Rmodel, k, Pnl)
        model_name = "M"
        params = get_BF_params(index, model_name)
        Rp, Sigma, DeltaSigma, aDS = get_delta_sigma(params, z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name) #Mpc/h comoving and Msun h/pc^2 com.
        
        axarr[i][j].errorbar(Rinds, DS, DSerr, ls='', marker='.', c='k')
        axarr[i][j].errorbar(Rbad, DSbad, DSerrbad, ls='', marker='.', c='k', mfc='w')
        axarr[i][j].loglog(Rp/(h*(1+z)), DeltaSigma*h*(1+z)**2, ls='-', c='r')
        axarr[i][j].set_yscale('log')
        axarr[i][j].set_xscale('log')
        axarr[i][j].set_xticks(xlabels)
axarr[0][0].set_xlim(0.08, 30.)
axarr[-1][1].set_xlabel(r"$R\ [{\rm Mpc}]$")
axarr[1][0].set_ylabel(r"$\Delta\Sigma\ [{\rm M_\odot/pc^2}]$")
plt.subplots_adjust(wspace=0.25)
plt.show()
