import numpy as np
from helper_functions import *
from likelihood import *
import models

#Set up the assumptions
cosmo = get_cosmo()
h = cosmo['h'] #Hubble constant

def find_best_fit(args, bfpath):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov = args
    guess = get_model_start(model_name)
    import scipy.optimize as op
    nll = lambda *args: -lnprob(*args)
    result = op.minimize(nll, guess, args=(args,), tol=1e-2)
    print "Best fit being saved at :\n%s"%bfpath
    print result
    print "\tresults: ",result['x']
    print "\tsuccess = %s"%result['success']
    outmodel = models.model_swap(result['x'], model_name)
    np.savetxt(bfpath, outmodel)
    return 

if __name__ == "__main__":
    print "do stuff"
