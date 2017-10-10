import numpy as np
import helper_functions as HF
import clusterwl

#R perpendicular
Rp = np.logspace(-2, 2.4, 1000, base=10) #Mpc/h

"""
Switch between models.
"""
def model_swap(params, model_name):
    defs = HF.get_model_defaults()
    if name is "Mc":
        lM, c = params
    if name is "M":
        lM = params
        c = defs['c']
    return lM, c

def get_delta_sigma(params, z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name):
    lM, c = model_swap(params, model_name)
    Om = cosmo['om']
    h = cosmo['h']
    M = 10**lM
    xi_nfw   = clusterwl.xi.xi_nfw_at_R(Rmodel, M, c, om)
    bias = clusterwl.bias.bias_at_M(M, k, Plin, om)
    xi_2halo = clusterwl.xi.xi_2halo(bias, xi_mm)
    xi_hm    = clusterwl.xi.xi_hm(xi_nfw, xi_2halo)
    Sigma  = clusterwl.deltasigma.Sigma_at_R(Rp, Rmodel, xi_hm, M, c, om)
    DeltaSigma = clusterwl.deltasigma.DeltaSigma_at_R(Rp, Rp, Sigma, M, c, om)
    ave_DeltaSigma = np.zeros((len(Redges)-1))
    clusterwl.averaging.average_profile_in_bins(Redges, Rp, DeltaSigma, ave_DeltaSigma)
    return Rp, Sigma, DeltaSigma, ave_DeltaSigma
