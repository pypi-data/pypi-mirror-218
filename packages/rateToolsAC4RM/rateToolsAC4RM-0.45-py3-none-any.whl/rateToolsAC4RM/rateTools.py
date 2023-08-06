
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import math


  
# function that takes a rate and a time i and return the discount factor to time i
def d(i,rate):
  ## your code here ##
  di=(1/(1+rate)**i)
  ####################
  return di



"""Let's use our discount factors to present value, or "pv" a set of cash flows."""

def pv(cf,dcf):
  ## your code here
  pv=0
  for flow,discount in zip(cf,dcf):
    pv=pv+flow*discount
  ##
  return pv


# Function that if given rate to time i, and time i+1, and i, will cacluate the 
# forward disctount rate from time i to i+1
def fwd(i,ratei,rateiplus):  
  ## your code here. #########
  ## remember fwd0=rate[1]. ##
  if i==0:
     fwdi=rateiplus
  else:
    fwdi=((1+rateiplus)**(i+1))*((1+ratei)**-i)-1
  ############################
  return fwdi


## given rates and time t's get forwards ##
def rates2fwds(yc):
  tData={"t":yc['t']-1}
  fwds=pd.DataFrame(tData)

  # make a copy of our yc and define some values we can loop over 
  yc1=yc.copy()
  yc1['fwd']=''  
  yc1['rate1'] = yc1['rate'].shift(1)
  yc1['rate2'] = yc1['rate']

  for index, rates in yc1.iterrows():
    yc1['fwd'][index]=fwd(index,rates['rate1'],rates['rate2'])

  fwds['rate']=yc1['fwd']  
  return fwds



## given forwards generate correpsonding dcd's  ##
def fwds2dcf(fwds):
  tData={"t":fwds['t']+1}
  dcfs=pd.DataFrame(tData)

  dcfs['dcf']=[0]*10
  dcfDummy=1
  for index, fwd2 in fwds.iterrows():
    dcfDummy=dcfDummy/(1+fwd2['rate'])
    dcfs['dcf'][index]=dcfDummy
 
  return dcfs




"""Thios is what we call a dv01, change in value due to a .01% change in interest rates up. Notivce the value change is negative, which is what we expect for increasing rates.

If we have a standard trading instruments, say a $1MM par swaps at current market rates, all the way out for each year, we can generate the forwars sensitities for our basis instruments and compare them against
"""

## Get the discount curves that correspond to each indpependently perturbed 
## forward rate at each time step
def dDCF(fwds):
  delta=.0001
  fwdsC=fwds.copy()
  dDCF=fwds2dcf(fwdsC)
  dDCF['dDCF0']=fwds2dcf(fwds)['dcf']
  fwdsC['rate'][1]=fwdsC['rate'][1]+delta
  dDCF['dDCF1']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][2]=fwdsC['rate'][2]+delta
  dDCF['dDCF2']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][3]=fwdsC['rate'][3]+delta
  dDCF['dDCF3']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][4]=fwdsC['rate'][4]+delta
  dDCF['dDCF4']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][5]=fwdsC['rate'][5]+delta
  dDCF['dDCF5']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][6]=fwdsC['rate'][6]+delta
  dDCF['dDCF6']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][7]=fwdsC['rate'][7]+delta
  dDCF['dDCF7']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][8]=fwdsC['rate'][8]+delta
  dDCF['dDCF8']=fwds2dcf(fwdsC)['dcf']
  fwdsC=fwds.copy()
  fwdsC['rate'][9]=fwdsC['rate'][9]+delta
  dDCF['dDCF9']=fwds2dcf(fwdsC)['dcf']

  #dDCF=pd.DataFrame({base,dDCF0})
  return dDCF


## using perturbed discount curves calculate the change in cashflow value pv() for each forward rate
def dFWDS(cashflows,ddcf):
  dFWD=ddcf[['t']]-1
  baseVal=pv(cashflows,ddcf['dcf'])
  dFWD1=[]
  dFWD1.append(pv(cashflows,ddcf['dDCF0'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF1'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF2'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF3'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF4'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF5'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF6'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF7'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF8'])-baseVal)
  dFWD1.append(pv(cashflows,ddcf['dDCF9'])-baseVal)

  dFWD['dFWD']=dFWD1

  #dFWD['dd']=ddcf['dDCF0']   

  return dFWD


# Define a function to generate a bullet swap  given tenor, rate, face amount
def bulletSwap(tenor,coupon,face):
  bullet= coupon*face*np.asarray([1]*tenor)
  bullet[tenor-1]=bullet[tenor-1]+face
  return bullet


# create a function that given a yeild curve it generates in sequence
# each of the term swap cashflows moving from year 1 to the last year
# following function assumes rates are all 1 year apart
from scipy.optimize import fsolve

def swapMkt(yc,face=1000):
  swap=[]
  for  year in yc.itertuples():
    # solve for breakeven swap rate given dcf
    be = lambda rate : pv(bulletSwap(year.t,rate,1000),yc['dcf'])-1000.  
    rateBE=fsolve(be,year.rate) 
    swap.append([year.t,rateBE[0],bulletSwap(year.t,rateBE,face)])
  return swap


# This function generate the forward rate sensitivity for a set of standard
# 1 year forward starting swaps defined by a market. it's complicated because
# it needs to use two differentnearby swaps in the series to calulate the sensitivity
# the end result is the series of sensitivities for each of the years out to 10 years
# for eacxh forward swap. Most values are zero or near zero.
def swap1YrFwds01(swapMkt,ddcf):
  swap1YrFwds01=[]
  #for swap in swapMkt.reverse:
  for index, swap in enumerate(swapMkt):
    start,rate,cashflow=swap
    if index < len(swapMkt)-1:
      end,rate,cashflow2=swapMkt[index+1]
      swap1YrFwds01.append([start,end,dFWDS(cashflow2,ddcf)['dFWD']-dFWDS(cashflow,ddcf)['dFWD']])

  return swap1YrFwds01



from itertools import zip_longest

def swap1YrFwdsCF(fwdMkt,ddcf):
  swap1YrFwdsCF=[]
  #for swap in swapMkt.reverse:

  for index, swap in enumerate(fwdMkt):
    start,rate,cashflow=swap
    if index < len(fwdMkt)-1:
      end,rate,cashflow2=fwdMkt[index+1]
      #print(cashflow2-cashflow)
      result = [sum(x) for x in zip_longest(cashflow, -cashflow2, fillvalue=0)]
      swap1YrFwdsCF.append(result)

  return swap1YrFwdsCF



# sum cashflows across periods
def sumCF(assets):
  totCF=np.zeros(10)
  from operator import add
  for t,rate,cf in assets:
    cfa=np.array(cf)
    totCF[:len(cfa)]+=cfa
  return(totCF)

#######################
# Now we define a function that finds the hedges for the total cashflows
# that breaks it into hedge ratios for each forward swap by starting at
# the end and works into front of curve

import pandas as pd
def portfolioHedge(portFwd01,mktFwd01):
  hRatio=[]

  for i in range(9,0,-1):
    tmpPortFwd01=portFwd01['dFWD'].iloc[i]
    tmpMktFwd01=np.array(mktFwd01[i-1][2])
    hr=tmpPortFwd01/tmpMktFwd01[i]
    hRatio.insert(0,[i,i+1,hr])
  hrDF=pd.DataFrame(hRatio)
  hrDF.columns=["start","end","fwdHR"]

  return(hrDF)
#######################
# Now let's turn our hedge into an equivalent cashflow for our swaps hedges
def hedgeCF(fwdMktCF,hedgeRatios):
  cfs=[]
  for cf,hr in zip(fwdMktCF,hedgeRatios):
    cfs.append([0,0,[ x * hr for x in cf ]])
  
  return(sumCF(cfs))


# here we define a function to generate the 
def psaSimulation(ppmts,psa,pSchedule,pmts,rate,up=1.5,dn=.5):
  # ppmts - regular principal payments w/o prepay
  # psa - periodic prepayment rates
  # pSchedule - prinipal schedule assuming no prepay
  # total - payment interest+principal for no prepay
  # rate - mortgage rate
  # up - up move multiplier for psa sim
  # dn - dn move multiplier for psa sim

  cfPSAup=[]
  cfPSAdn=[]
  cfPSA=[]
  cf=[]

  # initialize for loop
  bal=balUp=balDn=1000
  rateLoss=0
  rateLossUp=0
  rateLossDn=0
  for ppmt,cpr,currBal,pmt in zip(ppmts,psa,principalSched['schedule'],pmts):
    
    tmpBal=bal+ppmt-cpr*bal-rateLoss
    if tmpBal>0:
      cfPSA.append(-pmt)
      bal=tmpBal
      rateLoss=(currBal-bal)*rate
    else:
      cfPSA.append(bal)
      bal=0

    tmpBalup=balUp+ppmt-up*cpr*balUp-rateLossUp
    if tmpBalup>0:
      cfPSAup.append(-pmt)
      balUp=tmpBalup
      rateLossUp=(currBal-balUp)*rate
    else:
      cfPSAup.append(balUp)
      balUp=0

    tmpBalDn=balDn+ppmt-dn*cpr*balDn-rateLossDn
    if tmpBalDn>0:
      cfPSAdn.append(-pmt)
      balDn=tmpBalDn
      rateLossDn=(currBal-balDn)*rate
    else:
      cfPSAdn.append(balDn)
      balDn=0

  psaSim=pd.DataFrame({'cf': -pmt,'psaCF':cfPSA,'psaUpCF':cfPSAup,'psaDnCF':cfPSAdn})
  
  return(psaSim)