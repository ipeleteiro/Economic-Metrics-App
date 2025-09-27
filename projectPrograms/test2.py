# the follwing code will probably just be copy-pasted into the OWID file to ease the joining of all csv files
import wbgapi as wb
import pandas as pd
from owid import catalog
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

df = catalog.find('benefits')
print(df)
df.to_csv('searches.csv')

df = pd.DataFrame(catalog.find('unemployment').load())
#current_number_of_cases_of_alcohol_use_disorders_per_100_000_people__in_both_sexes_aged_all_ages
df.to_csv('unemployment.csv')


# below line is used to find metrics in the WB catalog that include 'GDP'
#print(wb.series.info(q='GDP'))

df = wb.data.DataFrame('SL.UEM.TOTL.ZS')
df.to_csv('ue.csv')

print(wb.series.info(q='benefits'))


