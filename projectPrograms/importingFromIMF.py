import requests
import pandas as pd

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'CompactData/IFS/M.GB.PMP_IX' # adjust codes here

# key = 'CompactData/[seriesName]/[frequency].[referenceArea].[dataIndicator]'

# Navigate to series in API-returned JSON data
data = (requests.get(f'{url}{key}').json()
        ['CompactData']['DataSet']['Series'])

key2 = 'CompactData/IFS/M.GB.PCPI_IX'
data2 = data = (requests.get(f'{url}{key2}').json()
        ['CompactData']['DataSet']['Series'])

print(data2['Obs'][-1]) # Print latest observation
#  obserbation^    ^latest one
# 'Obs' is the key for all obsevations in the 'data' dictionary


# Create pandas dataframe from the observations
data_list = []
for obs in data['Obs']:
        data_list.append([obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')])
# for every observation in data, get the time period and observation value and store it in data_list
# data list looks like this: [[timePeriod1, dataVal1], [timePeriod2, dataVal2], ...]


df = pd.DataFrame(data_list, columns=['date', 'value'])
# create dataframe with date and value
pd.to_datetime(df['date'])
df = df.set_index('date')
df['value'].astype('float')

# Save cleaned dataframe as a csv file
df.to_csv('UK_import_price_index.csv', header=True)


