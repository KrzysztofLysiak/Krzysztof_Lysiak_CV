import pandas as pd
import re
import matplotlib.pyplot as plt
import math
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
#import tensorflow_decision_forests as tfdf

print(tf.__version__)

##### Reading Poland market ()


df = pd.read_csv(r'C:\Users\krzys\Downloads\Wynagrodzenia.csv')
df_prices = pd.read_csv(r'C:\Users\krzys\Downloads\Ceny_mieszkan.csv')
df_meters = pd.read_csv(r'C:\Users\krzys\Downloads\Ilosc_sprzedanych_metrow.csv')
df_avg_prices = pd.read_csv(r'C:\Users\krzys\Downloads\avg_prices.csv')
df_apartment_area = pd.read_csv(r'C:\Users\krzys\Downloads\Apartment_area.csv')
df_unemployment = pd.read_csv(r'C:\Users\krzys\Downloads\Unemployment.csv')
df_inflation = pd.read_csv(r'C:\Users\krzys\Downloads\Inflation.csv')


##### Reading UK market (this is AI training data)


df_UK_Prices = pd.read_excel(r'C:\Users\krzys\Downloads\UK House price index (1).xlsx', sheet_name='Average price')
df_UK_Number_of_Dwellings = pd.read_excel(r'C:\Users\krzys\Downloads\Number_and_density_of_dwellings_by_borough.xlsx', sheet_name='Number of dwellings')
df_UK_Dwellings_per_hectare = pd.read_excel(r'C:\Users\krzys\Downloads\Number_and_density_of_dwellings_by_borough.xlsx', sheet_name='Dwellings per hectare')
df_UK_earnings = pd.read_excel(r'c:\Users\krzys\Downloads\earnings-residence-borough.xlsx', sheet_name='Full-time, Weekly')
df_UK_jobs = pd.read_excel(r'c:\Users\krzys\Downloads\jobs-and-job-density.xlsx', sheet_name='Jobs')
df_UK_population_estimates = pd.read_excel(r'c:\Users\krzys\Downloads\ons-mye-custom-age-tool-2020.xlsx', sheet_name='Single year of age')
df_UK_interest_rate = pd.read_csv(r'c:\Users\krzys\Downloads\interest_rates.csv')

def UK_Data_processing(df):
  counter =0
  small_counter =0

  for i in df.iloc[:,1]:
    if pd.isna(i):
      df.iloc[counter,1] = str('Space' + str(small_counter))
      small_counter = small_counter + 1
    counter =counter + 1 

  df = df.fillna(0)
  df = df.set_index(df.columns[1])
  df = df.drop(df.columns[0], axis=1)

  End = df.index.get_loc('Westminster')
  df = df.iloc[:End+1,:].sum()
  df = df.astype(int)

  return df


##### Cleaning data from Poland



def cleaning_data_of_another_type(df):

  counter = 0
  rows = []

  for i in range(0,3):
    rows.append(df.iloc[counter,0].split(";"))
    del rows[counter][:2]
    counter = counter + 1

  
  columns = []
  
  rows = [sublist for sublist in [[item for item in sublist if item not in [None, '']] for sublist in rows] if sublist]
  l = int(math.floor(len(rows[0])/13))+1

  for i in range(1,l):
    for j in range(2011,2024):
      columns.append(j)

  df = pd.DataFrame(data = rows, columns = columns)
  
  return df

# Salary

dataframe = pd.DataFrame()

def cleaning_data(df):


  variable = df.columns[0].replace(';', '').replace('""', '"').replace('[zł]', '').replace("[-]", "").replace("' '", "").replace('ogółem', '').replace(",", '')[10:].split('"')
  i = 0
  split_values = []


  for j in df.index:
    if isinstance(j, int):
      split_values.append(str(j)+';')
    else:  
      split_values.append(str(j))
    
    split_values[i] = split_values[i].replace("'","").replace(')','').replace(' ','').split(';')
    del split_values[i][0:2]
    i = i +1

  for i in variable:
    if i == ' ':continue
    if i == '':continue
    df[i] = None

  variable.pop(-1)
  df = df.drop(df.columns[0], axis = 1)

  dataframe = pd.DataFrame(data = split_values, columns = variable)
  dataframe = dataframe.replace(",",".",regex=True)
  dataframe = dataframe.apply(lambda x: x + '.00' if len(str(x)) == 4 else x)
  dataframe = dataframe.apply(lambda x: x.astype(float))

  return dataframe

dataframe = cleaning_data(df)

### Prices

df_prices = cleaning_data_of_another_type(df_prices)

### Meters

rows = []
columns = []
counter = 0

for i in df_meters.index:
  k = str(str(i) + df_meters.iloc[0].to_string(index=False)).replace('"','').replace(" ","")
  k = re.sub(r'\[m2\]|do40m2|rynekwtórny|od80|od40|1do60m2|1m2|ogółem|"','', k)
  k = re.sub(r"''","", k)
  k = k.replace(';;;',';').replace(';;',';')
  k = k.split(';')
  rows.append(k)
  rows[counter] = list(map(lambda x:x[:-2] if ',' in x  else x,rows[counter]))

  counter = counter + 1


for i in range(1,16):
  for j in range(2011,2024):
    columns.append(j)

rows = list(filter(lambda x: x not in ('', None, 0,'a-z','"',','), rows))
rows = [[item for item in sublist if item] for sublist in rows]
rows = [[item.rstrip("',") for item in sublist] for sublist in rows]
rows = [row[2:] for row in rows]


df_meters = pd.DataFrame(data = rows, columns = columns)

rows =[]

### Average prices 

df_avg_prices = cleaning_data_of_another_type(df_avg_prices)

### Unemployment

df_unemployment = cleaning_data_of_another_type(df_unemployment)

### Inflation

df_inflation = cleaning_data(df_inflation)


### Apartment Area
rows = []
counter = 0 


for i in range(0,3):

  rows.append(((str(df_apartment_area.index[counter]) + str(df_apartment_area.iloc[counter].values)).replace("\\","").replace("]","").replace(" ","").replace(")","").replace("'","").replace(" ","").replace("' '","")).split(";"))
  del rows[counter][:2]
  rows[counter] = list(map(lambda x:x[:-2] if ',' in x  else x,rows[counter]))
  counter = counter + 1
  
rows = [sublist for sublist in [[item for item in sublist if item not in [None, '']] for sublist in rows] if sublist]
df_apartment_area = pd.DataFrame(data = rows, columns = columns)


###### Processing training data

df_UK_Prices = df_UK_Prices['LONDON']

## Numbers of Dwellings
counter =0
small_counter =0

for i in df_UK_Number_of_Dwellings.iloc[:,1]:
  if pd.isna(i):
    df_UK_Number_of_Dwellings.iloc[counter,1] = str('Space' + str(small_counter))
    small_counter = small_counter + 1
  counter =counter + 1 

df_UK_Number_of_Dwellings = df_UK_Number_of_Dwellings.fillna(0)
df_UK_Number_of_Dwellings = df_UK_Number_of_Dwellings.set_index(df_UK_Number_of_Dwellings.columns[1])
df_UK_Number_of_Dwellings = df_UK_Number_of_Dwellings.drop(df_UK_Number_of_Dwellings.columns[0], axis=1)

End = df_UK_Number_of_Dwellings.index.get_loc('Westminster')
df_UK_Number_of_Dwellings = df_UK_Number_of_Dwellings.iloc[:End+1,:].sum()
df_UK_Number_of_Dwellings = df_UK_Number_of_Dwellings.astype(int)


## Size of the apartment area


## earnings

datas = []
for i in range(2001,20024):
  datas.append(str(i))

df_UK_earnings = df_UK_earnings.iloc[2:,1:].reset_index(drop=True)
df_UK_earnings = df_UK_earnings.set_index(df_UK_earnings['Area'])
df_UK_earnings = df_UK_earnings.loc['London']
mask = df_UK_earnings.iloc[1:].astype(float) > 50
df_UK_earnings = df_UK_earnings.iloc[1:][mask]

## jobs

df_UK_jobs = df_UK_jobs.iloc[1:,1:].reset_index(drop=True)
df_UK_jobs = df_UK_jobs.set_index('Area',drop=True)
End = df_UK_jobs.index.get_loc('Westminster')
df_UK_jobs = df_UK_jobs.iloc[:End+1,:].sum().astype(int)

## population

df_UK_population_estimates.index = df_UK_population_estimates.iloc[:,1]
df_UK_population_estimates.columns = df_UK_population_estimates.iloc[1]

df_UK_population_estimates = df_UK_population_estimates.drop(df_UK_population_estimates.columns[0:2], axis=1)
df_UK_population_estimates = df_UK_population_estimates.drop(df_UK_population_estimates.index[1])
df_UK_population_estimates.columns.name = None
df_UK_population_estimates.index.name = None

##


df_meters = df_meters.map(lambda x: x.split('\\')[0])
df_meters = df_meters.replace(r'\D', '', regex=True)

##### Analysist


## Random Forest



## Neutral network



##### Ploting
'''
i=0
plt.figure(figsize=(8, 6))
for index, row in dataframe.iterrows():
    plt.plot(dataframe.columns, dataframe.iloc[i], marker='o', label=f'Row {index}')
    i = i +1

plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()
'''