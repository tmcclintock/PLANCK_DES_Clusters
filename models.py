import numpy as np
import helper_functions as HF
import clusterwl

#R perpendicular
Rp = np.logspace(-2, 2.4, 1000, base=10) #Mpc/h

"""
Switch between models.
"""
def model_swap(params, model_name, z=0.2):
    defs = HF.get_model_default()
    if model_name is "Mc":
        lM, c = params
    if model_name is "M":
        lM = params
        c = HF.get_concentration(10**lM, z)
    return lM, c

def get_delta_sigma(params, z, cosmo, k, Plin, Pnl, Rmodel, xi_mm, Redges, model_name):
    lM, c = model_swap(params, model_name, z)
    print lM, c
    om = cosmo['om']
    h = cosmo['h']
    M = 10**lM
    #print "here", M, lM
    xi_nfw   = clusterwl.xi.xi_nfw_at_R(Rmodel, M, c, om)
    bias = clusterwl.bias.bias_at_M(M, k, Plin, om)
    xi_2halo = clusterwl.xi.xi_2halo(bias, xi_mm)
    xi_hm    = clusterwl.xi.xi_hm(xi_nfw, xi_2halo)
    Sigma  = clusterwl.deltasigma.Sigma_at_R(Rp, Rmodel, xi_hm, M, c, om)
    DeltaSigma = clusterwl.deltasigma.DeltaSigma_at_R(Rp, Rp, Sigma, M, c, om)
    ave_DeltaSigma = np.zeros((len(Redges)-1))
    #Redges are already in Mpc/h physical
    clusterwl.averaging.average_profile_in_bins(Redges, Rp, DeltaSigma, ave_DeltaSigma)
    return Rp, Sigma, DeltaSigma, ave_DeltaSigma
