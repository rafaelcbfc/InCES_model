#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 17:03:06 2020

@author: rafael
"""
###Imports
import sys

sys.path.append("/Users/rafael/Documents/GitHub/InCES-model/Industrial_communities")
import Hofstede
import random
import numpy as np


###Calculation varialbes
pool_countries = ["AUS", "BRA", "IRA", "JPN", "NLD", "USA"]
country = pool_countries[5]
discount_rate = getattr(Hofstede, country + "_discount_rate")
sunshine = getattr(Hofstede, country + "_sunshine")
wind_dist =getattr(Hofstede, country + "_wind_dist")  
solar_costs = getattr(Hofstede, country + "_solarCosts")
wind_costs = getattr(Hofstede, country + "_windCosts")
decision_style = getattr(Hofstede, country + "_Decision_style")
decision_rule = getattr(Hofstede, country + "_Decision_rule")
solar_OM = getattr(Hofstede, country + "_solar_OM")
wind_OM = getattr(Hofstede, country + "_wind_OM")
 
gridtariff = getattr(Hofstede, country + "_gridtariff")
wind_threshold = 5000 #in KW, minimum value to make it a possibility for wind energy production - https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2019/May/IRENA_Renewable-Power-Generations-Costs-in-2018.pdf?la=en&hash=99683CDDBC40A729A5F51C20DA7B6C297F794C5D
depreciation_period = 20

pool_financial_investments = ["feed-in-tariff", "tax-incentive", "tradable-certificates"]

financial_investment = "tradable-certificates" 

if financial_investment == 'feed-in-tariff':
    fit = 3 #2.1 , 2.5, 3
    tx = 0
    tax_incentive = 1-tx
    tgc = 0

elif financial_investment == "tax-incentive":
    fit = 1
    tx = 0.6 #0.2, 0.4, 0.6
    tax_incentive = 1-tx
    tgc = 0

elif financial_investment == "tradable-certificates":
    fit = 1
    tx = 0
    tax_incentive = 1-tx
    tgc = 0.025 #0.015, 0.02, 0.025

else:
    fit = 1
    tx = 0
    tax_incentive = 1-tx
    tgc = 0


###Calculations
def cbaCalc(me): #Individual Cost benefit: Buy from grid or produce energy?
##Variables 
  #Global vairables
    rev0, rev1, rev2, rev3, cos1, cos2, cos3 = [], [], [], [], [], [], []
    gridtariff1 = random.choice(gridtariff)
    solar_implement_Costs =random.choice(solar_costs) * tax_incentive
    wind_implement_Costs =random.choice(wind_costs) * tax_incentive
    solar_OM1 = random.choice(solar_OM)
    wind_OM1 = random.choice(wind_OM)
    option_i = 0
    test = 0

  #Individuals variable  
    annual_demand = me.energy
    
##Case 0 - Grid energy
    r0 = gridtariff1 * annual_demand
    
    for i in range(depreciation_period):
        rev0.append(r0)
        
    Baseline_cost = np.npv(discount_rate, rev0)
    
##Case 1 - All solar
    solar_energy1 = annual_demand
    installation_solar1 = solar_energy1 / sunshine
    investment_solar1 = installation_solar1 * solar_implement_Costs
    OM_solar1 = solar_OM1 * (investment_solar1/(solar_energy1 * depreciation_period)) * solar_energy1
    LCOE_solar1 = (investment_solar1 + OM_solar1 * depreciation_period)/(solar_energy1 * depreciation_period) 
    
    r1 = gridtariff1 * solar_energy1 + (tgc *solar_energy1)                           #Produce energy
    c1=  OM_solar1
    
    for i in range(depreciation_period):
        rev1.append(r1)
        cos1.append(c1)
    
    revenue1 = np.npv(discount_rate, rev1)
    costs1 = investment_solar1 + np.npv(discount_rate, cos1)
    NPV1 = revenue1-costs1
    
##Case 2 - All wind 
    if annual_demand > wind_threshold:
        test = 1
    wind_energy2 = annual_demand
    installation_wind2 = wind_energy2 / wind_dist
    investment_wind2 = installation_wind2 * wind_implement_Costs
    OM_wind2 = wind_OM1 * wind_energy2
    LCOE_wind2 = (investment_wind2 + OM_wind2 * depreciation_period)/(wind_energy2 * depreciation_period) 
    
    r2 = gridtariff1 * wind_energy2 + (tgc *wind_energy2)                          #Produce energy
    c2 =  OM_wind2
    
    for i in range(depreciation_period):
        rev2.append(r2)
        cos2.append(c2)
    
    revenue2 = np.npv(discount_rate, rev2)
    costs2 = investment_wind2 + np.npv(discount_rate, cos2)
    NPV2 = revenue2-costs2
    
##Case 3- Mixed sources
  #wind
    energy3_wind = (int(annual_demand/wind_threshold)*wind_threshold)
    installation_wind3 = energy3_wind / wind_dist
    investment_wind3 = installation_wind3 * wind_implement_Costs
    OM_wind3 = wind_OM1 * energy3_wind
    try:
        LCOE_wind3 = (investment_wind3 + OM_wind3 * depreciation_period)/(energy3_wind * depreciation_period)
    except: 
        LCOE_wind3 = 0
    
  #Solar
    energy3_solar = annual_demand % wind_threshold
    installation_solar3 = energy3_solar / sunshine
    investment_solar3 = installation_solar3 * solar_implement_Costs
    OM_solar3 = solar_OM1 * (investment_solar3/(energy3_solar * depreciation_period)) * energy3_solar
    try:
        LCOE_solar3 = (investment_solar3 + OM_solar3 * depreciation_period)/(energy3_solar * depreciation_period) 
    except:
        LCOE_solar3 = 0
        
    r3 = gridtariff1 * annual_demand + (tgc * annual_demand)                                                                      #Produce energy 
    c3 =  OM_wind3 + OM_solar3 
    
    for i in range(depreciation_period):
        rev3.append(r3)
        cos3.append(c3)
    
    revenue3 = np.npv(discount_rate, rev3)
    costs3 = (investment_solar3 + investment_wind3) + np.npv(discount_rate, cos3)    
    NPV3 = revenue3 - costs3
    
    ratio_solar = energy3_solar/(energy3_wind+energy3_solar)
    ratio_wind = energy3_wind / (energy3_wind+energy3_solar)
    
##Avaliation
  #Variables
    if test == 1:
        NPV2 = -100000
    costs = [costs1, costs2, costs3]
    produce = [NPV1, NPV2, NPV3]
    me.max_re = max(produce)
  #1st evaluation => is grid energy more expensive than construct RE?
    count = 0
    for cost in costs:
        if Baseline_cost >= cost: #Grid energy expensier
           count = count + 1
        if max(produce) >= 0: #at least one positive NPV for producing
            count = count + 1
    
    if count == 0:
        me.cba_lvl = 1 #Grid energy is cheaper than RE and no positive NPV
    
  #2nd evaluation => I am going for renewable, but is it better to produce to my self?
    if me.cba_lvl != 1:
        me.cba_lvl = 2 #Producing energy is the preference
        option_i = produce.index(max(produce))
        
        #What is the levelized cost of my option  
        if option_i == 0:
            me.LCOE = LCOE_solar1
        if option_i == 1:
            me.LCOE = LCOE_wind2
        if option_i == 2:
            me.LCOE = (LCOE_solar3 * ratio_solar + LCOE_wind3 * ratio_wind)
    
    return me.LCOE
    return me.cba_lvl

def cbaCalcCom(me, peer):
    if me.LCOE < peer.premium:
        me.cba_lvlc = 0
    else:
        me.cba_lvlc = 1
                

def cbaCalcPeer(me, peer):
##Variables    
  #Global variables
    rev1, rev2, rev3, cos1, cos2, cos3 = [], [], [], [], [], []
    gridtariff2 = random.choice(gridtariff)
    solar_implement_Costs =random.choice(solar_costs)  * tax_incentive
    wind_implement_Costs =random.choice(wind_costs)  * tax_incentive
    solar_OM2 = random.choice(solar_OM)
    wind_OM2 = random.choice(wind_OM)
    test = 0
  #Peered variables
    annual_demand = (me.energy + peer.energy)
    
##Case 1 - All solar
    solar_energy1 = annual_demand
    installation_solar1 = solar_energy1 / sunshine
    investment_solar1 = installation_solar1 * solar_implement_Costs
    OM_solar1 = solar_OM2 * (investment_solar1/(solar_energy1 * depreciation_period)) * solar_energy1
    LCOE_solar1 = (investment_solar1 + OM_solar1 * depreciation_period)/(solar_energy1 * depreciation_period) 
    
    r1 = gridtariff2 * solar_energy1 + (tgc * solar_energy1)                        #Produce energy
    c1=  OM_solar1
    
    for i in range(depreciation_period):
        rev1.append(r1)
        cos1.append(c1)
    
    revenue1 = np.npv(discount_rate, rev1)
    costs1 = (0.15 * investment_solar1) + (0.7 * investment_solar1) + np.npv(discount_rate, cos1)
    NPVp1 = revenue1-costs1

   
##Case 2 - All wind
    if annual_demand > wind_threshold:
        test = 1
    wind_energy2 = annual_demand
    installation_wind2 = wind_energy2 / wind_dist
    investment_wind2 = installation_wind2 * wind_implement_Costs
    OM_wind2 = wind_OM2 * wind_energy2
    LCOE_wind2 = (investment_wind2 + OM_wind2 * depreciation_period)/(wind_energy2 * depreciation_period) 
    
    r2 = gridtariff2 * wind_energy2 + (tgc * wind_energy2)                      #Produce energy
    c2 =  OM_wind2
    
    for i in range(depreciation_period):
        rev2.append(r2)
        cos2.append(c2)
     
        
    revenue2 = np.npv(discount_rate, rev2)
    costs2 = (0.15 * investment_wind2) + (0.7 * investment_wind2) + np.npv(discount_rate, cos2)    
    NPVp2 = revenue2 - costs2
   
    
##Case 3- Mixed sources
  #wind
    wind_energy3 = (int(annual_demand/wind_threshold)*wind_threshold)
    installation_wind3 = wind_energy3 / wind_dist
    investment_wind3 = installation_wind3 * wind_implement_Costs
    OM_wind3 = wind_OM2 * wind_energy3
    try:
        LCOE_wind3 = (investment_wind3 + OM_wind3 * depreciation_period)/(wind_energy3 * depreciation_period)
    except: 
        LCOE_wind3 = 0
    
  #Solar
    solar_energy3 = annual_demand % wind_threshold
    installation_solar3 = solar_energy3 / sunshine
    investment_solar3 = installation_solar3 * solar_implement_Costs
    OM_solar3 = solar_OM2 * (investment_solar3/(solar_energy3 * depreciation_period)) * solar_energy3
    try:
        LCOE_solar3 = (investment_solar3 + OM_solar3 * depreciation_period)/(solar_energy3 * depreciation_period) 
    except:
        LCOE_solar3 = 0
         
    r3 = gridtariff2 * annual_demand + (tgc * annual_demand)                                                                        #Produce energy 
    c3 =  OM_wind3 + OM_solar3 
    
    for i in range(depreciation_period):
        rev3.append(r3)
        cos3.append(c3)
    
    revenue3 = np.npv(discount_rate, rev3)
    costs3 = ((0.15 * investment_solar3) + (0.7 * investment_solar3) + (0.15 * investment_wind3) + (0.7 * investment_wind3)) + np.npv(discount_rate, cos3)
    NPVp3 = revenue3-costs3
    
##Avaliation
    if test == 1:
       NPVp2 = -100000
    produce_p = [NPVp1, NPVp2, NPVp3]
    
    
  #1st evaluation => doing business with peer is more advantageous?
    count2 = 0 
    max_npvp = max(produce_p)
    if max_npvp <= 0: #Negative NPV
        count2 = count2 + 1
    if me.max_re > max_npvp: #Producing individually is cheaper
        count2 = count2 + 1
    if peer.max_re > max_npvp: #Producing in group is cheaper
        count2 = count2 + 1
    
    if count2 > 0:
        me.cba_lvlp == 1 #producing individually is cheper than in group
    
  #2nd evaluation => if we are doing business, produce is a good alternative?
    if me.cba_lvlp != 1:
       me.cba_lvlp = 2 #Producing has a higher NPV

   
def projectSelector(me):
    me.energy_solar = 0
    me.energy_wind = 0
    me.incentive_fit = 0
    me.incentive_tax = 0
    me.project_cost = 0 
    me.project_tariff = 0
    me.project_margin = 0
    option_c = 0
##Variables    
  #Global variables  
    rev1, rev2,rev3,rg1_fit, rg1_tgc, rg2_fit, rg2_tgc, rg3_fit, rg3_tgc, cos1, cos2, cos3 = [], [], [], [], [], [], [], [], [], [], [], []
    gridtariff3 = random.choice(gridtariff)
    solar_implement_Costs =random.choice(solar_costs)  * tax_incentive
    wind_implement_Costs =random.choice(wind_costs)  * tax_incentive
    solar_OM3 = random.choice(solar_OM)
    wind_OM3 = random.choice(wind_OM)
    solar_gov_imp = solar_implement_Costs/tax_incentive
    wind_gov_imp = wind_implement_Costs/tax_incentive
    test = 0
    
  #Community variables  
    me.project_cost = 0
    project_cba = 0
    annual_demand = me.energy *1.1
    
##Case 1 - All solar
    energy1 = annual_demand
    installation_solar1 = energy1 / sunshine
    investment_solar1 = installation_solar1 * solar_implement_Costs
    investment_solarg1 = installation_solar1 * solar_gov_imp
    OM_solar1 = solar_OM3 * (investment_solar1/(energy1 * depreciation_period)) * energy1
    LCOE_solar1 = (investment_solar1 + OM_solar1 * depreciation_period)/(energy1 * depreciation_period) 
    
    r1 = gridtariff3 * energy1 + (tgc * energy1)                        #Produce energy
    c1=  OM_solar1
    g1_fit = r1/fit
    g1_tgc = (tgc * energy1)
    
    for i in range(depreciation_period):
        rev1.append(r1)
        cos1.append(c1)
        rg1_fit.append(g1_fit)
        rg1_tgc.append(g1_tgc)
        
    revenue1 = np.npv(discount_rate, rev1)
    costs1 = ((0.3/float(len(me.members))) * investment_solar1) + (0.7 * investment_solar1) + np.npv(discount_rate, cos1)

    NPVc1= revenue1-costs1
    marginc1 = (revenue1 - costs1)/(revenue1 *100)
    
    tgc_inc1 = np.npv(discount_rate, rg1_tgc)
    if g1_fit != r1:
        fit1 = np.npv(discount_rate, rg1_fit)
    else:
        fit1 = 0
    if investment_solarg1 != investment_solar1:
        tax_inc1 = investment_solarg1  
    else:
        tax_inc1 = 0
    

##Case 2 - All wind
    if annual_demand > wind_threshold:
        test = 1
    energy2 = annual_demand
    installation_wind2 = energy2 / wind_dist
    investment_wind2 = installation_wind2 * wind_implement_Costs
    investment_windg2 = installation_wind2 * wind_gov_imp
    OM_wind2 = wind_OM3 * energy2
    LCOE_wind2 = (investment_wind2 + OM_wind2 * depreciation_period)/(energy2 * depreciation_period) 
    
    r2 = gridtariff3 * energy2 + (tgc * energy2)                       #Produce energy
    c2 =  OM_wind2
    g2_fit = r2/fit
    g2_tgc = (tgc * energy2)
    
    for i in range(depreciation_period):
        rev2.append(r2)
        cos2.append(c2)
        rg2_fit.append(g2_fit)
        rg2_tgc.append(g2_tgc)
    
    revenue2 = np.npv(discount_rate, rev2)
    costs2 = ((0.3/float(len(me.members))) * investment_wind2) + (0.7 * investment_wind2) + np.npv(discount_rate, cos2)
    
    NPVc2 = revenue2 - costs2
    marginc2 = (revenue2 - costs2)/(revenue2 *100)
    
    tgc_inc2 = np.npv(discount_rate, rg2_tgc)
    if g2_fit != r2:
        fit2 = np.npv(discount_rate, rg2_fit)
    else:
        fit2 = 0
    if investment_windg2 != investment_wind2:
        tax_inc2 = investment_windg2
    else:
        tax_inc2 = 0
    
##Case 3- Mixed sources
  #wind
    energy3_wind = (int(annual_demand/wind_threshold)*wind_threshold)
    installation_wind3 = energy3_wind / wind_dist
    investment_wind3 = installation_wind3 * wind_implement_Costs
    investment_windg3 = installation_wind3 * wind_gov_imp
    OM_wind3 = wind_OM3 * energy3_wind
    try:
        LCOE_wind3 = (investment_wind3 + OM_wind3 * depreciation_period)/(energy3_wind * depreciation_period)
    except: 
        LCOE_wind3 = 0
    
  #Solar
    energy3_solar = annual_demand % wind_threshold
    installation_solar3 = energy3_solar / sunshine
    investment_solar3 = installation_solar3 * solar_implement_Costs
    investment_solarg3 = installation_solar3 * wind_gov_imp
    OM_solar3 = solar_OM3 * (investment_solar3/(energy3_solar * depreciation_period)) * energy3_solar
    try:
        LCOE_solar3 = (investment_solar3 + OM_solar3 * depreciation_period)/(energy3_solar * depreciation_period) 
    except:
        LCOE_solar3 = 0
        
    r3 = gridtariff3 * annual_demand + (tgc * annual_demand)                                                                    #Produce energy 
    c3 =  OM_wind3 + OM_solar3 
    g3_fit = r3/fit
    g3_tgc = (tgc * annual_demand)

    for i in range(depreciation_period):
        rev3.append(r3)
        cos3.append(c3)
        rg3_fit.append(g3_fit)
        rg3_tgc.append(g3_tgc)
    
    revenue3 = np.npv(discount_rate, rev3)
    costs3 = (((0.3/float(len(me.members))) * investment_solar3) + (0.7 * investment_solar3) + ((0.3/float(len(me.members))) * investment_wind3) + (0.7 * investment_wind3)) + np.npv(discount_rate, cos3)
    
    NPVc3 = revenue3 - costs3
    marginc3 = (revenue3 - costs3)/(revenue3 *100)
    
    ratio_solar = energy3_solar/(energy3_wind+energy3_solar)
    ratio_wind = energy3_wind / (energy3_wind+energy3_solar)

    tgc_inc3 = np.npv(discount_rate, rg3_tgc)
    if g3_fit != r3:
        fit3 = np.npv(discount_rate, rg3_fit)
    else:
        fit3 = 0
    if investment_solarg3 != investment_solar3:
        tax_inc3 = investment_solarg3 + investment_windg3
    else:
        tax_inc3 = 0
   
##Avaliation
    if test == 1:
        NPVc2 = -1000000
    produce_c = [NPVc1, NPVc2, NPVc3]
    
  #1st evaluation => doing business with peer is more advantageous?
    count2 = 0 
    max_npvc = max(produce_c)
    if max_npvc <= 0: #Negative NPV
        count2 = count2 + 1
    
    if count2 > 0:
        project_cba = 1 #producing individually is cheper than in group
        me.project_margin = - 1
        me.project_cost = annual_demand * gridtariff3
  #2nd evaluation => if we are doing business, produce is a good alternative?
    if project_cba != 1:
       project_cba = 2 #Producing has a high NPV
       option_c = produce_c.index(max(produce_c))
    
#What is the levelized cost of my option  
    if option_c == 0: #Solar
        me.project_tariff0 = LCOE_solar1
        me.project_tariff1 = r1
        me.project_margin = max(marginc1)
        me.project_cost = costs1
        me.energy_solar = energy1 * 20
        me.energy_wind = 0
        me.incentive_fit = fit1
        me.incentive_tax = tax_inc1
        me.incentive_tgc = tgc_inc1
    if option_c == 1: #Wind
        me.project_tariff0 = LCOE_wind2
        me.project_tariff1 = r2
        me.project_margin = max(marginc2)
        me.project_cost = costs2
        me.energy_solar = 0
        me.energy_wind = energy2 * 20
        me.incentive_fit = fit2
        me.incentive_tax = tax_inc2
        me.incentive_tgc = tgc_inc2
    if option_c == 2: #Mixed
        me.project_tariff0 = (LCOE_solar3 * ratio_solar + LCOE_wind3 * ratio_wind)
        me.project_tariff1 = r3
        me.project_margin = max(marginc3)
        me.project_cost = costs3
        me.energy_solar = energy3_solar * 20
        me.energy_wind = energy3_wind * 20
        me.incentive_fit = fit3
        me.incentive_tax = tax_inc3
        me.incentive_tgc = tgc_inc3
        


    




