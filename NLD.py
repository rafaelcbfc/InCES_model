#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rafael
"""

import sys
sys.path.append("/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities")
import pandas as pd
import numpy as np
import statistics
from scipy import stats
from scipy.stats import uniform
import matplotlib.pylab as plt
from itertools import cycle, islice


###Definitions
##Variables
Active_communities = pd.DataFrame()
Communities_members = pd.DataFrame()
Total_solar_energy = pd.DataFrame()
Total_wind_energy = pd.DataFrame()
Total_renewable_energy = pd.DataFrame()
Exit_members = pd.DataFrame()
Invested_capital = pd.DataFrame()
LCOE = pd.DataFrame()
Policy_indicator = pd.DataFrame()
Governmental_expenditure = pd.DataFrame() 

##Tick set
ticks = list(range(0,20000))


###Datasets import
##NETHERLANDS
#Scenario 0 - No incentives
N00 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S0 - No incentive/Model_run_NLD_S0.csv")
#Scenario 1 - FIT
N11 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S1 - FIT/Model_run_NLD_S1-01.csv")
N12 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S1 - FIT/Model_run_NLD_S1-02.csv")
N13 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S1 - FIT/Model_run_NLD_S1-03.csv")
#Scenario 2 - TAX
N21 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S2 - TAX/Model_run_NLD_S2-01.csv")
N22 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S2 - TAX/Model_run_NLD_S2-02.csv")
N23 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S2 - TAX/Model_run_NLD_S2-03.csv")
#Scenario 3 - TGC
N31 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S3 - TGC/Model_run_NLD_S3-01.csv")
N32 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S3 - TGC/Model_run_NLD_S3-02.csv")
N33 = pd.read_csv(r"/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities/Modelrun/S3 - TGC/Model_run_NLD_S3-03.csv")


#### Datacube creation
###Scenario 0 - Data Frame
##Collectio
N0, N1, N2, N3, N4, N5, N6, N7, N8, N9, N10, N11, N12, N13, N14, N15, N16, N17, N18, N19 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
#tick1
for i in ticks[1::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N1.append(z)
#tick2
for i in ticks[2::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N2.append(z)
#tick3
for i in ticks[3::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N3.append(z)
#tick4
for i in ticks[4::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N4.append(z)
#tick5
for i in ticks[5::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N5.append(z)
#tick6
for i in ticks[6::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N6.append(z)
#tick7
for i in ticks[7::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N7.append(z)
#tick8
for i in ticks[8::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N8.append(z)
#tick9
for i in ticks[9::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N9.append(z)
#tick10
for i in ticks[10::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N10.append(z)
#tick11
for i in ticks[11::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N11.append(z)
#tick12
for i in ticks[12::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N12.append(z)
#tick13
for i in ticks[13::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N13.append(z)
#tick14
for i in ticks[14::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N14.append(z)
#tick15
for i in ticks[15::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N15.append(z)
#tick16
for i in ticks[16::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N16.append(z)
#tick17
for i in ticks[17::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N17.append(z)
#tick18
for i in ticks[18::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N18.append(z)
#tick19
for i in ticks[19::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N19.append(z)
#tick0
for i in ticks[0::20]: 
    z = N00["ActiveCommunities"].iloc[i]
    N0.append(z)