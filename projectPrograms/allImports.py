from owid import catalog
import wbgapi as wb
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# the following further reduces the data (so only the G7 and the years I need are used) and places all of this on a new dataframe df1
def selectCountries(df_in):
    countries = ["United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
    df_out = df_in.loc[("Italy",2000):("Italy",2023)]
    for country in countries:
        temp = df_in.loc[(country,2000):(country,2023)]
        df_out = pd.concat([df_out, temp])
    return df_out

# used to format the WB dataframes to the way the WB dataframes are
def formatWB(df_in):
    countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
    tuples = []
    for country in countries:
        for year in range(2000,2020):
            tuples.append((country,year))

    # creates multilevel index for each country with the years 2000-2022
    index = pd.MultiIndex.from_tuples(tuples, names=["country", "year"])

    dataList = []
    for country in ['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN']:
        for year in range(2000,2020):
            year = 'YR'+str(year)
            dataList.append(df_in.loc[country, year])

    df_out = pd.Series(dataList, index=index)
    return df_out



def indexOWID(dfFull, dfCut):
    countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
    dfFull = dfFull.swaplevel()
    for year in range(2000,2020):
        dfInfo = dfFull.loc[year].describe()
        mean = dfInfo.loc['mean']    # finds mean for that year
        stdDev = dfInfo.loc['std']   # finds standard deviation for that year
        
        minval = mean - 2*stdDev                     # creates a minimum -2 stds away from mean
        maxval = mean + 2*stdDev                     # creates a maximum +2 stds away from mean

        dfCut = dfCut.swaplevel()                    # levels are swaped so the years can be searched for
        if minval > min(dfCut.loc[year]):
            minval = min(dfCut.loc[year])
        if maxval < max(dfCut.loc[year]):
            maxval = max(dfCut.loc[year])            # ensures the G7 do not surpass the maximum
        dfCut = dfCut.swaplevel()
        length = maxval - minval

        dfCut = dfCut.sort_index()             ####### PerformanceWarning: indexing past lexsort depth may impact performance.
        for country in countries:
            dfCut.loc[country,year] = (dfCut.loc[country,year]-minval)/length
    return dfCut


def indexWB(dfFull, dfCut):
    countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
    dfInfo = dfFull.describe()                       # gets all the summary statistics of the dataframe
    for year in range(2000,2020):
        mean = dfInfo["YR"+str(year)].loc['mean']    # finds mean for that year
        stdDev = dfInfo["YR"+str(year)].loc['std']   # finds standard deviation for that year
        minval = mean - 2*stdDev                     # creates a minimum -2 stds away from mean
        maxval = mean + 2*stdDev                     # creates a maximum +2 stds away from mean

        dfCut = dfCut.swaplevel()
        if minval > min(dfCut.loc[year]):
            minval = min(dfCut.loc[year])
        if maxval < max(dfCut.loc[year]):
            maxval = max(dfCut.loc[year])            # ensures the G7 do not surpass the maximum
        dfCut = dfCut.swaplevel()
        length = maxval - minval
        for country in countries:
            dfCut.loc[country,year] = (dfCut.loc[country,year]-minval)/length
    return dfCut


# used to reduce repeated code when importing data from OWID
def finiliseOWID(df_in, metricName, tableName):
    df = df_in[metricName]
    dfAll = df.sort_index()
    df = selectCountries(dfAll)
    df = indexOWID(dfAll, df)
    df = df.rename(tableName)
    return df
# I will only apply this function to the metrics from prototype 2 and onwards, to show the growth of the code

# same as finilisedWB, used to reduce repeated code
def finiliseWB(code, reName):
    regions = ['WLD', 'HIC', 'OED', 'AFE', 'AFW', 'ARB', 'CEB', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 'EUU', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'PRE', 'PST', 'SAS', 'SSA', 'SSF', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC', 'IBD']
    dfAll = wb.data.DataFrame(code)
    dfAll = dfAll.drop(index=regions)
    df = wb.data.DataFrame(code,['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
    df_out = formatWB(df)
    df_out = df_out.rename(reName)
    df_out = indexWB(dfAll, df_out)
    df_out = df_out.sort_index()
    return df_out                       
# I will only apply this function to the metrics from prototype 3 and onwards, to show the growth of the code

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# print(catalog.find('life'))
# the above line is used to find the different metrics in the catalog

df = pd.DataFrame(catalog.find('life_expectancy', version="2022-11-30").load())
# df holds all the data from OWID regarding life expectancy

df = df["life_expectancy_0"]
df = df.rename("life_expectancy")
# here I am narrowing down the data to only hold the specific metric I need

countries = ["United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
dfLife = selectCountries(df)
dfLife = indexOWID(df, dfLife)




df = pd.DataFrame(catalog.find('neoplasms__particulate_matter_pollution__both_sexes__age').load())
df = df["dalys_from_neoplasms_attributed_to_particulate_matter_pollution_per_100_000_people_in__both_sexes_aged_age_standardized"]
df = df.sort_index()

dfPol = selectCountries(df)
dfPol = indexOWID(df, dfPol)

dfPol = dfPol.rename("pollution")
# remaning the table so the column is easier to identify (and much shorter)



# tables got updated, so there are now multiple 'inequality' tables, so I need to specify further
#df = pd.DataFrame(catalog.find('inequality').load())
df = pd.DataFrame(catalog.find('inequality', version="2023-01-27").load())
df.to_csv('inequality.csv')

dfIncomeInqAll = df["p0p100_gini_pretax"]
dfWealthInqAll = df["p0p100_gini_wealth_extrapolated"]

dfIncomeInq = selectCountries(dfIncomeInqAll)
dfIncomeInq = indexOWID(dfIncomeInqAll, dfIncomeInq)
dfIncomeInq = dfIncomeInq.rename("income_inequality")

dfWealthInq = selectCountries(dfWealthInqAll)
dfWealthInq = indexOWID(dfWealthInqAll, dfWealthInq)
dfWealthInq = dfWealthInq.rename("wealth_inequality")

# while the following is a lot of repeated code, 
# making a function for it would complicate the process of finding the data and selecting the metric 
# so I opted to simply write the code out

df = pd.DataFrame(catalog.find('global_carbon_budget', version='2023-09-28').load())
dfCarbon = finiliseOWID(df, 'consumption_emissions_per_capita', "global_carbon_budget")

df = pd.DataFrame(catalog.find('greenhouse_gas_emissions_by_sector', dataset='emissions_by_sector').load())
df.to_csv('greenhouse.csv')
dfGreenhouse = finiliseOWID(df, 'total_ghg_emissions_including_lucf_per_capita', "greenhouse_gas_emissions")

df = pd.DataFrame(catalog.find('renewable_electricity_capacity', version='2023-06-26').load())
dfRenewable = finiliseOWID(df, 'total_renewable_energy', "renewable_electricity_capacity")

df = pd.DataFrame(catalog.find('child_mortality', version='2020-12-19').load())
df = df.set_index(['country', 'year'])
dfChildMor = finiliseOWID(df, 'probability_of_death_under_5', "child_mortality")



# ~~~~~~~~~~~~~~~~~~~~~~ PROTOTYPE 3 METRICS ~~~~~~~~~~~~~~~~~~~~~~

df = pd.DataFrame(catalog.find('alcohol_use_disorders__both_sexes__all_ages', dataset='gbd_mental_health').load())
dfAlcohol = finiliseOWID(df, 'current_number_of_cases_of_alcohol_use_disorders_per_100_000_people__in_both_sexes_aged_all_ages', 'alcohol_use_disorders')

df = pd.DataFrame(catalog.find('all_causes__bullying_victimization__both_sexes__all_ages').load())
dfBullying = finiliseOWID(df, 'dalys_from_all_causes_attributed_to_bullying_victimization_per_100_000_people_in__both_sexes_aged_all_ages', "bullying_victimisation")

df = pd.DataFrame(catalog.find('all_causes__drug_use__both_sexes__all_ages').load())
dfDrugs = finiliseOWID(df, 'dalys_from_all_causes_attributed_to_drug_use_per_100_000_people_in__both_sexes_aged_all_ages', "drug_use")

df = pd.DataFrame(catalog.find('all_causes__environmental_occupational_risks__both_sexes__all_ages').load())
dfEnvOccRisk = finiliseOWID(df, 'dalys_from_all_causes_attributed_to_environmental_occupational_risks_per_100_000_people_in__both_sexes_aged_all_ages', "environmental_occupational_risks")

df = pd.DataFrame(catalog.find('all_causes__high_body_mass_index__both_sexes__all_ages').load())
dfBMI = finiliseOWID(df, 'dalys_from_all_causes_attributed_to_high_body_mass_index_per_100_000_people_in__both_sexes_aged_all_ages', "body_mass_index")

df = pd.DataFrame(catalog.find('all_causes__unsafe_water_source__both_sexes__all_ages').load())
dfUnsafeWater = finiliseOWID(df, 'dalys_from_all_causes_attributed_to_unsafe_water_source_per_100_000_people_in__both_sexes_aged_all_ages', "unsafe_water")

df = pd.DataFrame(catalog.find('pedestrian_road_injuries__both_sexes__all_ages', dataset='gbd_cause').load())
dfRoadInj = finiliseOWID(df, 'dalys_from_pedestrian_road_injuries_per_100_000_people_in__both_sexes_aged_all_ages', "pedestrian_road_injuries")

df = pd.read_csv('mentalHealth.csv')
df = df.set_index(['country', 'year', 'sex', 'age'])
df = df.sort_index()     

# vvvvvvvvvvvvvvvvvvvvv fixing mental health import
df = pd.read_csv('mentalHealth.csv')
df = df.set_index(['country', 'year', 'sex', 'age'])

df = df.xs('Both', level=2, drop_level=False)
df = df.xs('All ages', level=3, drop_level=False)
df = df.reset_index(level='sex')
df = df.reset_index(level='age')
df = df.drop(['sex', 'age'], axis=1)

df = df.sort_index()
dfCut = selectCountries(df)

# add together share_anxiety_disorders,share_bipolar_disorders,share_depressive_disorders,share_eating_disorders,share_schizophrenia_disorders
df['sum'] = df[['share_anxiety_disorders','share_bipolar_disorders','share_depressive_disorders','share_eating_disorders','share_schizophrenia_disorders']].sum(axis=1)
dfCut['sum'] = dfCut[['share_anxiety_disorders','share_bipolar_disorders','share_depressive_disorders','share_eating_disorders','share_schizophrenia_disorders']].sum(axis=1)

df = indexOWID(df['sum'], dfCut['sum'])

dfMentalHealth = df.rename('mental_health')
# ^^^^^^^^ mental health import

df = pd.DataFrame(catalog.find('fertility_rate').load())
dfFertility = finiliseOWID(df, 'fertility_rate', "fertility_rate")

df = pd.DataFrame(catalog.find('education_lee_lee').load())
dfLiteracy = finiliseOWID(df, 'mf_primary_enrollment_rates_combined_wb', "literacy_rate")
#mf_primary_enrollment_rates_combined_wb







# below line is used to find metrics in the WB catalog that include 'GDP'
#print(wb.series.info(q='GDP'))




dfAll = wb.data.DataFrame('NY.GDP.MKTP.CD')
dfAll.to_csv('gdphelp.csv')
# ensuring only countries are used for the indexing, not regions
regions = ['WLD', 'HIC', 'OED', 'AFE', 'AFW', 'ARB', 'CEB', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 'EUU', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'PRE', 'PST', 'SAS', 'SSA', 'SSF', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC', 'IBD']
dfAll = dfAll.drop(index=regions)
# from the WB data, import the table NY.GDP.MKTP.CN, including only the follwing countries
df = wb.data.DataFrame('NY.GDP.MKTP.CD',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDP = formatWB(df)
dfGDP = dfGDP.rename("GDP")
dfGDP = indexWB(dfAll, dfGDP)
dfGDP = dfGDP.sort_index()


dfAll = wb.data.DataFrame('NY.GDP.PCAP.CD')
dfAll = dfAll.drop(index=regions)
df = wb.data.DataFrame('NY.GDP.PCAP.CD',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDPperC = formatWB(df)
dfGDPperC = dfGDPperC.rename("GDP_per_capita")
dfGDPperC = indexWB(dfAll, dfGDPperC)
dfGDPperC = dfGDPperC.sort_index()

dfAll = wb.data.DataFrame('NY.GDP.MKTP.PP.CD')
dfAll = dfAll.drop(index=regions)
df = wb.data.DataFrame('NY.GDP.MKTP.PP.CD',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDP_PPP = formatWB(df)
dfGDP_PPP = dfGDP_PPP.rename("GDP_PPP")
dfGDP_PPP = indexWB(dfAll, dfGDP_PPP)
dfGDP_PPP = dfGDP_PPP.sort_index()




dfGNI = finiliseWB('NY.GNP.MKTP.CD','GNI')  # great
dfGNIperC= finiliseWB('NY.GNP.PCAP.CD', 'GNI_per_capita') # great
dfGNI_PPP= finiliseWB('NY.GNP.MKTP.PP.CD', 'GNI_PPP')  # great
dfInflation= finiliseWB("FP.CPI.TOTL.ZG", 'inflation')   # great
dfCAperGDP= finiliseWB("BN.CAB.XOKA.GD.ZS", 'current_account_pct_GDP')      # have to adjust for negative values
dfRnDExpPerGDP= finiliseWB("GB.XPD.RSDV.GD.ZS", 'R&D_expenditure_pct_GDP')    # great
dfGovExpPerGDP= finiliseWB("NE.CON.GOVT.ZS", 'government_expenditure_pct_GDP')  # great
dfGovExpHelPerGDP= finiliseWB("SH.XPD.GHED.GD.ZS", 'health_pct_government_expenditure')   # beauty
dfRuralPerPop= finiliseWB("SP.RUR.TOTL.ZS", 'rural_living_pct_popoluation')     # pinacle of beauty
dfMigration= finiliseWB("SM.POP.NETM", 'migration')          # great
dfLabourPar= finiliseWB("SL.TLF.CACT.ZS", 'labour_participation')      # great
dfGovEffectiveness= finiliseWB("GE.EST", 'government_effectiveness')     # missing 2001 from all countries, rest is great
dfGovExpEduPerGDP= finiliseWB("SE.XPD.TOTL.GD.ZS", 'education_pct_government_expenditure')  # Canada 2003, 2004, 2006
dfIncomeTax= finiliseWB("GC.TAX.YPKG.CN", 'income_tax')       # no data for Japan
dfTimeForTaxes= finiliseWB("IC.TAX.DURS", 'hours_to_file_taxes')      # no data for 2000-2004,  for US n Japan no data for 2000-2013
dfInterestRate= finiliseWB("FR.INR.RINR",'interest_rates')    # VERY LACKING,,,
dfPoliticalStability= finiliseWB("PV.EST", 'political_stability')          # quite good, no 2001 data
dfTradeTransportQuality= finiliseWB("LP.LPI.INFR.XQ", 'trade_transport_quality')    # only data for 6 years, prob taken every 2 years
dfForestArea= finiliseWB("AG.LND.FRST.ZS", 'forest_area')     # amazing
dfForestDepleteion= finiliseWB("NY.ADJ.DFOR.GN.ZS", 'forest_depletion_pct_GNI')  # beatiful
dfUnemployment = finiliseWB('SL.UEM.TOTL.ZS', 'unemployment')

# joining all tables into the Current table

# track fo stuff that didnt work :(
# df = df.drop_duplicates(keep='first')
# df.index = df.index.drop_duplicates(keep='first') (Length mismatch: Expected axis has 192 elements, new values have 168 elements)
#df = df.groupby(df.index).first()
'''
for df in [dfLife, dfPol, dfIncomeInq, dfWealthInq, dfGDP, dfGDPperC, dfGDP_PPP, dfCarbon, dfGreenhouse, dfChildMor, dfRenewable]:
    df['country', 'year'] = df.index
    df = df.drop_duplicates(keep='first')
    df.set_index = df['country', 'year']
    df = df.drop(['country', 'year'])
'''
# turns out it was an error within the country selection function

tableList = [dfLife, dfPol, dfIncomeInq, dfWealthInq, dfGDP, dfGDPperC, dfGDP_PPP, dfCarbon, dfGreenhouse, dfChildMor, dfRenewable, dfGNI,dfGNIperC,dfGNI_PPP,dfInflation,dfCAperGDP,dfRnDExpPerGDP,dfGovExpPerGDP,dfGovExpEduPerGDP,dfGovExpHelPerGDP,dfGovEffectiveness,dfIncomeTax,dfTimeForTaxes,dfRuralPerPop,dfInterestRate,dfMigration,dfLabourPar,dfPoliticalStability,dfTradeTransportQuality, dfForestArea, dfForestDepleteion, dfFertility, dfMentalHealth, dfRoadInj, dfBMI, dfUnsafeWater, dfBullying, dfEnvOccRisk, dfAlcohol, dfDrugs, dfLiteracy, dfUnemployment]
current = pd.concat(tableList, axis=1, join='inner')
current.to_csv("Current.csv", header=True)
