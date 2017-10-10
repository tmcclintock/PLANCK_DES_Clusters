import numpy as np
from models import *

def lnprior(params, model_name):
    lM, c = model_swap(params, model_name)
    if lM < 11.0 or lM > 18.0 or c <= 0.0 or c > 20.0: return -np.inf
    return 0

def lnlike(params, args):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov = args
    Rp, Sigma, DS, aveDS = get_delta_sigma(params, z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name)
    h = cosmo['h']

    #Convert to Mpc physical
    X = DS - aveDS*h*(1+z)**2
    return -0.5*np.dot(X, np.dot(icov, X))

def lnprob(params, args):
    z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name, R, DS, icov, cov = args
    lpr = lnprior(params, model_name)
    if not np.isfinite(lpr): return -np.inf
    return lpr + lnlike(params, args)
