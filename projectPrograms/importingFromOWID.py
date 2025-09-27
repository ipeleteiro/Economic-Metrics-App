from owid import catalog
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


df = catalog.find('greenhouse_gas_emissions_by_sector')
print(df)
df.to_csv('searches.csv')



df = pd.DataFrame(catalog.find('alcohol_use_disorders__both_sexes__all_ages', dataset='gbd_mental_health').load())
#current_number_of_cases_of_alcohol_use_disorders_per_100_000_people__in_both_sexes_aged_all_ages
df.to_csv('alcoholUse.csv')

df = pd.DataFrame(catalog.find('all_causes__bullying_victimization__both_sexes__all_ages').load())
#dalys_from_all_causes_attributed_to_bullying_victimization_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('bullying.csv')

df = pd.DataFrame(catalog.find('all_causes__drug_use__both_sexes__all_ages').load())
#dalys_from_all_causes_attributed_to_drug_use_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('drugUse.csv')

df = pd.DataFrame(catalog.find('all_causes__environmental_occupational_risks__both_sexes__all_ages').load())
#dalys_from_all_causes_attributed_to_environmental_occupational_risks_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('envOccRisk.csv')

df = pd.DataFrame(catalog.find('all_causes__high_body_mass_index__both_sexes__all_ages').load())
#dalys_from_all_causes_attributed_to_high_body_mass_index_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('BMI.csv')

df = pd.DataFrame(catalog.find('all_causes__unsafe_water_source__both_sexes__all_ages').load())
#dalys_from_all_causes_attributed_to_unsafe_water_source_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('unsafeWater.csv')

df = pd.DataFrame(catalog.find('pedestrian_road_injuries__both_sexes__all_ages', dataset='gbd_cause').load())
#dalys_from_pedestrian_road_injuries_per_100_000_people_in__both_sexes_aged_all_ages
df.to_csv('pedestrianInjuries.csv')

df = pd.DataFrame(catalog.find('gbd_mental_health_prevalence_rate').load())
# add together share_anxiety_disorders,share_bipolar_disorders,share_depressive_disorders,share_eating_disorders,share_schizophrenia_disorders
df.to_csv('mentalHealth.csv')

df = pd.DataFrame(catalog.find('fertility_rate').load())
#fertility_rate
df.to_csv('fertility.csv')






df = pd.DataFrame(catalog.find('environmental_heat_and_cold_exposure__both_sexes__all_ages', dataset='gbd_cause').load())
df.to_csv('heatAndColdExposure.csv')

df = pd.DataFrame(catalog.find('living_planet_index').load())
df.to_csv('livingPlanetIndex.csv')

df = pd.DataFrame(catalog.find('global_carbon_budget', version='2023-09-28').load())
df.to_csv('globalCarbonBudget.csv')


df = pd.DataFrame(catalog.find('renewable_electricity_capacity', version='2023-06-26').load())
df.to_csv('renewableElectricityCapacity.csv')

df = pd.DataFrame(catalog.find('renewable_energy_investments').load())
df.to_csv('renewableEnergyInvestments.csv')


df = pd.DataFrame(catalog.find('unemployment').load())
df.to_csv('unemployment.csv')

df = pd.DataFrame(catalog.find('child_mortality', version='2020-12-19').load())
df.to_csv('childMortality.csv')


#print(catalog.find('life'))
# the above line is used to find the different metrics in the catalog

df = pd.DataFrame(catalog.find('life_expectancy', version="2022-11-30").load())
# df holds all the data from OWID regarding life expectancy

df = df["life_expectancy_0"]
# here I am narrowing down the data to only hold the specific metric I need


countries = ["United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]

# the following further reduces the data (so only the G7 and the years I need are used) and places all of this on a new dataframe df1
def selectCountries(df_in):
    df_out = df_in.loc[("Italy",2000):("Italy",2023)]
    for country in countries:
        temp = df_in.loc[(country,2000):(country,2023)]
        df_out = pd.concat([df_out, temp])
    return df_out

dfLife = selectCountries(df)

# then I turn the data into a .csv file
dfLife.to_csv('life_expectancy.csv', header=True)



'''Only above part will be documented probably'''

df = pd.DataFrame(catalog.find('neoplasms__particulate_matter_pollution__both_sexes__age').load())
df = df["dalys_from_neoplasms_attributed_to_particulate_matter_pollution_per_100_000_people_in__both_sexes_aged_age_standardized"]
df = df.sort_index()

dfPol = selectCountries(df)

dfPol = dfPol.rename("pollution")
# remaning the table so the column is easier to identify (and much shorter)

dfPol.to_csv("pollution.csv", header=True)



df = pd.DataFrame(catalog.find('inequality', version="2023-01-27").load())
df.to_csv('inequality.csv')

dfIncomeInq = df["p0p100_gini_posttax_nat_extrapolated"]
dfWealthInq = df["p0p100_gini_wealth_extrapolated"]

dfIncomeInq = selectCountries(dfIncomeInq)
dfIncomeInq = dfIncomeInq.rename("incomeInequality")
dfWealthInq = selectCountries(dfWealthInq)
dfWealthInq = dfWealthInq.rename("wealthInequality")

dfIncomeInq.to_csv("incomeInequality.csv", header=True)
dfWealthInq.to_csv("wealthInequality.csv", header=True)

# joining all tables into the Current table
current = pd.concat([dfLife, dfPol, dfIncomeInq, dfWealthInq], axis=1, join='inner')



