import numpy as np
from models import *

def lnprior(params, model_name):
    lM, c = model_swap(params, model_name)
    if lM < 11.0 or lM > 18.0 or c <= 0.0 or c > 20.0: return -np.inf
    return 0

def lnlike(params, args):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov, inds = args
    Rp, Sigma, DSmodel, aveDS = get_delta_sigma(params, z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name)
    h = cosmo['h']

    #print DS, np.sqrt(np.diagonal(cov))
    #Convert to Mpc physical
    X = DS - aveDS[inds]*h*(1+z)**2
    chi2 = -0.5*np.dot(X, np.dot(icov, X))
    #print "chi2 = %e"%chi2
    return chi2

def lnprob(params, args):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov, inds = args
    lpr = lnprior(params, model_name)
    if not np.isfinite(lpr): return -np.inf
    return lpr + lnlike(params, args)
