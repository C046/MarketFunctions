# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 17:53:04 2023

@author: hadaw
"""
from itertools import cycle
import numpy as np


# GROWTH RATE
def _gr(InitialEPSValue,FinalEPSValue=False):    
    # Define A Generator To Speed Up The Code
    def _GR(InitialEPSValue, FinalEPSValue):
        while True:
            # Subtract FinalEPSValue With InitialEPSValue then divide it by the InitialEPSValue
            yield [((np.subtract(fv,iv))/iv) for fv,iv in zip(FinalEPSValue,cycle(InitialEPSValue))]
      
        
    def _singleGR(InitialEPSValue):
        while True:
            yield [((np.subtract(fv,iv))/iv) for iv,fv in zip(InitialEPSValue[:-1], cycle(InitialEPSValue[1:]))]
            
            
    if FinalEPSValue != False:
        # Automate The Generator So That You Can Write Less Code
        for i in _GR(InitialEPSValue, FinalEPSValue):
            return i
    
    if FinalEPSValue == False:
        # Automate The Generator So That You Can Write Less Code
        for i in _singleGR(InitialEPSValue):
            return i
        
    
# PE RATIO
def _pe(MarketValuePerShare,EarningsPerShare):
    # Define A Generator To Speed Up The Code
    def _PE(MarketValuePerShare, EarningsPerShare):
        while True:
            # Divide MarketValuePerShare With EarningsPerShare
            yield [np.divide(mvp,eps) for mvp,eps in zip(MarketValuePerShare,cycle(EarningsPerShare))]
      
    # Automate The Generator So That You Can Write Less Code
    for i in _PE(MarketValuePerShare,EarningsPerShare):
        return i


# R-Expected earnings growth rate.
def _r(PE,ProjectedGrowthInEarnings):
    # Define A Generator To Speed Up The Code
    def _R(PE,ProjectedGrowthInEarnings):
        while True:
            # Divide PE with ProjectedGrowthInEarnings
            yield [np.divide(pe,pgs) for pe,pgs in zip(PE,cycle(ProjectedGrowthInEarnings))]
      
    # Automate The Generator So That You Can Write Less Code
    for i in _R(PE,ProjectedGrowthInEarnings):
        return i


# ESTIMATED PROFIT PER SHARE.
def _eps(NetIncome,PreferredDividends,AverageOutstandingCommonShares):
    # Define A Generator To Speed Up The Code
    def _EPS(NetIncome,PreferredDividends,AverageOutstandingCommonShares):
        while True:
            # Subtract NetIncome With Preferred Dividends Then Divide By the AverageOutstandingShares
            yield [((np.subtract(ni,_pd))/aocs) for ni,_pd,aocs in zip(NetIncome,cycle(PreferredDividends),cycle(AverageOutstandingCommonShares))]
      
    # Automate The Generator So That You Can Write Less Code
    for i in _EPS(NetIncome,PreferredDividends,AverageOutstandingCommonShares):
        return i


# INTRINSIC VALUE FUNCTION 
def _iv(eps,r,pe):
    # Define A Generator To Speed Up The Code
    def _INT(eps,r,pe):
        while True:
            # Add 1 to R Then Multiply EPS With R, Multiply This Value With PE Value
            yield [np.multiply(np.multiply(EPS,(1+R)),PE) for EPS,R,PE in zip(eps,cycle(r),cycle(pe))]
    
    # Automate The Generator So That You Can Write Less Code
    for i in _INT(eps,r,pe):
        return np.average(i)
    
        
        
        
  
   
        
# Establish arbitrary values
# This will take a total of 4 requests from an api.
NetIncome,PreferredDividends,AverageOutstandingCommonShares,MarketValuePerShare = [4,5,6,1,2,3],[3,2,1,5],[4,5,6,1,2,3],[4,5,6,1,2,3]

# Calculate on values
EPS = _eps(NetIncome,PreferredDividends,AverageOutstandingCommonShares)
PE = _pe(MarketValuePerShare,EPS)
ProjectedGrowthInEarnings = _gr(EPS)
R = _r(PE,ProjectedGrowthInEarnings)

# Finally return an intrinsic value
Intrinsic_value = _iv(EPS,R,PE)
