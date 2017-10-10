import numpy as np
from helper_functions import *
from likelihood import *
import models
import clusterwl

#Set up the assumptions
cosmo = get_cosmo()
h = cosmo['h'] #Hubble constant

model_name = "M"

def find_best_fit(args, bfpath):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov, inds = args
    guess = get_model_start(model_name)
    import scipy.optimize as op
    nll = lambda *args: -lnprob(*args)
    print "Starting BF"
    result = op.minimize(nll, guess, args=(args,), tol=1e-2, method="Powell")
    print "Best fit being saved at :\n%s"%bfpath
    print result
    print "\tresults: ",result['x']
    print "\tsuccess = %s"%result['success']
    outmodel = models.model_swap(result['x'], model_name)
    np.savetxt(bfpath, outmodel)
    return 

if __name__ == "__main__":
    bfbase = "results/bestfits/bf_cluster%d.txt"
    
    DS_all, err_all = get_all_data()
    N_bins = len(DS_all[0])
    Redges_Mpc, Rmid = HF.get_Redges_and_Rmid(N_bins) #Mpc physical
    zs = np.loadtxt("data/z.txt")
    N = 9 #len(zs)
    for i in range(N):
        if i < 0 or i > 9: continue
        z = zs[i]
        Redges = Redges_Mpc * h*(1+z) #Mpc/h comoving
        inds = get_good_indices(Rmid, DS_all[i])
        R, DS, err = Rmid[inds], DS_all[i, inds], err_all[i, inds]
        print DS, R
        cov = np.diag(err)
        icov = np.linalg.inv(cov)
        bfpath = bfbase%i
        k, Plin, Pnl = get_power_spectra(i)
        Rmodel = np.logspace(-2, 3, num=1000, base=10) 
        xi_mm = clusterwl.xi.xi_mm_at_R(Rmodel, k, Pnl)
        args = (z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov, inds)
        find_best_fit(args, bfpath)
