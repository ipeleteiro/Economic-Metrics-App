# the follwing code will probably just be copy-pasted into the OWID file to ease the joining of all csv files
import wbgapi as wb
import pandas as pd


# below line is used to find metrics in the WB catalog that include 'GDP'
#print(wb.series.info(q='GDP'))

fs = wb.series.info(q='gender')
print(fs)

# it's roughly a max of 10 queries per min
# they might be giving timeouts 

'''
GNI: NY.GNP.MKTP.CD
GNIperC: NY.GNP.PCAP.CD
GNI_PPP: NY.GNP.MKTP.PP.CD
Inflation: FP.CPI.TOTL.ZG
CA: BN.CAB.XOKA.CD
CAperGDP: BN.CAB.XOKA.GD.ZS
R&DExpPerGDP: GB.XPD.RSDV.GD.ZS
GovExpPerGDP: NE.CON.GOVT.ZS
GovExpEduPerGDP: SE.XPD.TOTL.GD.ZS
GovExpHelPerGDP: SH.XPD.GHED.GD.ZS
TourismExpPerM: ST.INT.XPND.MP.ZS
GovEffectiveness: GE.EST
GovDebtPerGDP: GC.DOD.TOTL.GD.ZS
TaxesTrade: GC.TAX.INTT.RV.ZS
IncomeTax: GC.TAX.YPKG.CN
TaxRevenuePerGDP: GC.TAX.TOTL.GD.ZS
TimeForTaxes: IC.TAX.DURS
RuralPerPop: SP.RUR.TOTL.ZS 
FirmsExpRD: IC.FRM.RSDV.ZS
InterestRate: FR.INR.RINR
Migration: SM.POP.NETM
LabourPar: SL.TLF.CACT.ZS  
AmbientAirPol: SH.STA.AIRP.P5 
Women3Decisions: SG.DMK.ALLD.FN.ZS
Literacy: SE.ADT.LITR.ZS 
PoliticalStability: PV.EST 
TradeTransportQuality: LP.LPI.INFR.XQ 
GenderEquality: IQ.CPA.GNDR.XQ
'''



# used to format the WB dataframes to the way the OWID dataframes are
def format(df_in):
    countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
    tuples = []
    for country in countries:
        for year in range(2000,2023):
            tuples.append((country,str(year)))

    # creates multilevel index for each country with the years 2000-2022
    index = pd.MultiIndex.from_tuples(tuples, names=["country", "year"])

    dataList = []
    for country in ['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN']:
        for year in range(2000,2023):
            year = 'YR'+str(year)
            dataList.append(df_in.loc[country, year])

    df_out = pd.Series(dataList, index=index)
    return df_out



dfAll = wb.data.DataFrame('NE.CON.GOVT.ZS')
# ensuring only countries are used for the indexing, not regions
regions = ['WLD', 'HIC', 'OED', 'AFE', 'AFW', 'ARB', 'CEB', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 'EUU', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'PRE', 'PST', 'SAS', 'SSA', 'SSF', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC', 'IBD']
dfAll = dfAll.drop(index=regions)
dfAll.to_csv('aaa.csv')


'''
# from the WB data, import the table NY.GDP.MKTP.CN, including only the follwing countries
df = wb.data.DataFrame('NY.GDP.MKTP.CN',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDP = format(df)
dfGDP = dfGDP.rename("GDP")
dfGDP.to_csv('GDP.csv',header=True)

df = wb.data.DataFrame('NY.GDP.PCAP.CN',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDPperC = format(df)
dfGDPperC = dfGDPperC.rename("GDP_per_capita")
dfGDPperC.to_csv('GDPperCapita.csv',header=True)

df = wb.data.DataFrame('NY.GDP.MKTP.PP.CD',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfGDP_PPP = format(df)
dfGDP_PPP = dfGDP_PPP.rename("GDP_PPP")
dfGDP_PPP.to_csv('GDP_PPP.csv',header=True)




# only has data for 2009
df = wb.data.DataFrame('EN.CLC.MDAT.ZS',['ITA','GBR', 'USA','FRA', 'JPN', 'DEU', 'CAN'])
dfExtremeWeather = format(df)
dfExtremeWeather = dfExtremeWeather.rename("GDP")
dfExtremeWeather.to_csv('ExtremeWeather.csv',header=True)'''