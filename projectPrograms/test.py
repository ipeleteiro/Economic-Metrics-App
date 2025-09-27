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
    print(df_out)
    df_out.to_csv(reName)
# I will only apply this function to the metrics from prototype 3 and onwards, to show the growth of the code


'''
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
dfForestArea= finiliseWB("AG.LND.FRST.ZS", 'forest_area')     # amazing
dfForestDepleteion= finiliseWB("NY.ADJ.DFOR.GN.ZS", 'forest_depletion_pct_GNI')  # beatiful
'''

# dfGovEffectiveness= finiliseWB("GE.EST", 'government_effectiveness')     # missing 2001 from all countries, rest is great
# dfGovExpEduPerGDP= finiliseWB("SE.XPD.TOTL.GD.ZS", 'education_pct_government_expenditure')  # Canada 2003, 2004, 2006
# dfIncomeTax= finiliseWB("GC.TAX.YPKG.CN", 'income_tax')       # no data for Japan
# dfTimeForTaxes= finiliseWB("IC.TAX.DURS", 'hours_to_file_taxes')      # no data for 2000-2004,  for US n Japan no data for 2000-2013
# dfInterestRate= finiliseWB("FR.INR.RINR",'interest_rates')    # VERY LACKING,,,
# dfPoliticalStability= finiliseWB("PV.EST", 'political_stability')          # quite good, no 2001 data
# dfTradeTransportQuality= finiliseWB("LP.LPI.INFR.XQ", 'trade_transport_quality')    # only data for 6 years, prob taken every 2 years







