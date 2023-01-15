# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 18:32:12 2023

@author: hadaw
"""
import numpy as np
import requests
from MarketFunctions import _iv, _eps, _r, _gr,_pe
import time
import math


def _c(symbol):
    s = ""
    for i in symbol:
        s = s+i.capitalize()
    
    return s


print("______________________________________________________________________________\n______________________________________________________________________________")
print("\n Welcome to my intrinsic value application for when I am at work. \n You are free to use this if you want, but I only find use for it personally.")
print("______________________________________________________________________________\n______________________________________________________________________________")

symbol = _c(str(input("\n Please type in a ticker symbol: ")))
api_key = "QNI1JU2CWCRNHF9T"


# ########## NET INCOME SCRIPT ###############
url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}'
activated = False
while activated == False:
    try:
        r = requests.get(url)
        for i in r.json():
            if i == 'Note':
                activated = False
            else:
                activated = True
        #print([i for i in r.json()])
        
    except Exception:
        time.sleep(5)

    
        
activated = False
NetIncome = [i["netIncome"] for i in r.json()["quarterlyReports"]]

############################################


##### COMMON STOCK SHARES OUTSTANDING SCRIPT ##############
url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}'

while activated == False:
    
    try:        
        r = requests.get(url)
        for i in r.json():
            if i == 'Note':
                activated = False
            else:
                activated = True
        
    except Exception:
        time.sleep(5)

activated = False
commonStockSharesOutstanding = [i["commonStockSharesOutstanding"] for i in r.json()["quarterlyReports"]]
############################################################################


##### PREFERRED DIVIDENDS SCRIPT ##############
url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}'

while activated == False:
     
    try:
        r = requests.get(url)
        for i in r.json():
            if i == 'Note':
                activated = False
            else:
                activated = True
        
    except Exception:
        time.sleep(5)

activated = False
Preferred_Dividends = [i["dividendPayoutCommonStock"] for i in r.json()["quarterlyReports"]]
P_Div = []

# Check for nones in this one.
for i in Preferred_Dividends:
    
    if i == str(None):
        i=0
        P_Div.append(i)
    else:
        if i != str(None):
            P_Div.append(i)


#####################share price################################################
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'

while activated == False:

    try:    
        r = requests.get(url)
        
        for i in r.json():
            if i == 'Note':
                activated = False
            else:
                activated = True
                
    except Exception:
        time.sleep(5)
################################################################################       
      
high = "2. high" 
low = "3. low"

MarketValuePerShare = r.json()[tuple(r.json())[1]]
MarketValuePerShare_low = [float(MarketValuePerShare[e][low]) for i,e in enumerate(MarketValuePerShare)]
MarketValuePerShare_high = [float(MarketValuePerShare[e][high]) for i,e in enumerate(MarketValuePerShare)]
NetIncome = np.array([float(i) for i in NetIncome])
P_Div = np.array([float(i) for i in P_Div])
commonStockSharesOutstanding = np.array([float(i) for i in commonStockSharesOutstanding])


eps = _eps(NetIncome,P_Div,commonStockSharesOutstanding)
pe_low = _pe(MarketValuePerShare_low,eps)
pe_high = _pe(MarketValuePerShare_high,eps)

ProjectedGrowthInEarnings = _gr(eps)
r_low = _r(pe_low,ProjectedGrowthInEarnings)
r_high = _r(pe_high,ProjectedGrowthInEarnings)

# Automate your brain.
if eps == 0.0:
    eps = -0.000000000000000000000000000000000000000000000000000000000000000001
    
Intrinsic_Value = (_iv(eps,r_low,pe_low)+_iv(eps,r_high,pe_high))/2


if Intrinsic_Value <=0:
    Intrinsic_Value = Intrinsic_Value*-1
    
if Intrinsic_Value/np.array(eps).mean() <=0:
    Intrinsic_Value = Intrinsic_Value/np.array(eps).mean()*-1

if Intrinsic_Value/np.array(eps).mean() >= 0:
    Intrinsic_Value = Intrinsic_Value/np.array(eps).mean()


Intrinsic_Value = (math.sqrt(Intrinsic_Value))/2


print(f"\n Your intrinsic value share price for {symbol} is: {Intrinsic_Value}")

#########################################################################
