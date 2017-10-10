import numpy as np


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

def get_Redges_and_Rmid(Nbins):
    Redges = np.logspace(np.log10(0.0323), np.log10(30.), num=Nbins+1)
    Rmid = (Redges[:-1] + Redges[1:])/2. #midpoint
    return Redges, Rmid

def fix_data(R, DS, err, scale_cut=False):
    if scale_cut: inds = np.invert(np.isnan(DS)) * (R > 0.2)
    else: inds = np.invert(np.isnan(DS))
    return R[inds], DS[inds], err[inds]