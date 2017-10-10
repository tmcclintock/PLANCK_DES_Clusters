import numpy as np
from models import *

cosmo = {"h":0.7, "om":0.3}
def get_cosmo():
    return cosmo

def get_lams():
    return 0

def get_zs():
    return 0.4 # BS value for now

def get_zs_and_lams():
    zs = get_zs()
    lams = get_lams()
    return zs, lams

#Data path
datapath = "data/dsig_data.txt"
errpath  = "data/error_bars.txt"

def get_DS_data():
    return np.loadtxt(datapath)

def get_DS_err():
    return np.loadtxt(errpath)

def get_all_data(cut_zeros=False):
    return get_DS_data(), get_DS_err()

def get_Redges_and_Rmid(Nbins): #Mpc physical
    Redges = np.logspace(np.log10(0.0323), np.log10(30.), num=Nbins+1)
    Rmid = (Redges[:-1] + Redges[1:])/2. #midpoint
    return Redges, Rmid

def fix_data(R, DS, err, scale_cut=False):
    if scale_cut: inds = np.invert(np.isnan(DS)) * (R > 0.2)
    else: inds = np.invert(np.isnan(DS))
    return R[inds], DS[inds], err[inds]

def get_good_indices(R, DS):
    P1 = np.invert(np.isnan(DS))
    P2 = (R > 0.2)
    P3 = (DS > 0)
    inds = P1*P2*P3
    return inds

def get_bad_indices(R, DS):
    return (R < 0.2)

def get_model_default():
    return {"c":5.0}

def get_model_start(model_name):
    defs = get_model_default()
    if model_name is "Mc": return 14.0, defs['c']
    else: return 14.0
    
def get_power_spectra(index):
    k = np.loadtxt("data/P_files/k.txt")
    Plin = np.loadtxt("data/P_files/plin_cluster%d.txt"%index)
    Pnl  = np.loadtxt("data/P_files/pnl_cluster%d.txt"%index)
    return k, Plin, Pnl

def get_BF_params(index, model_name):
    lM, c = np.loadtxt("results/bestfits/bf_cluster%d.txt"%index)
    if model_name is "M": return lM
    elif model_name is "Mc": return lM, c
