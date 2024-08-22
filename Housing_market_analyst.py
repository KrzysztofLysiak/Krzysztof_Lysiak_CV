import pandas as pd
import re
import matplotlib.pyplot as plt
import math
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models



##### Reading Poland market ()


df = pd.read_csv(r'C:\Users\krzys\Downloads\Wynagrodzenia.csv')
df_prices = pd.read_csv(r'C:\Users\krzys\Downloads\Ceny_mieszkan.csv')
df_meters = pd.read_csv(r'C:\Users\krzys\Downloads\Ilosc_sprzedanych_metrow.csv')
df_avg_prices = pd.read_csv(r'C:\Users\krzys\Downloads\avg_prices.csv')
df_apartment_area = pd.read_csv(r'C:\Users\krzys\Downloads\Apartment_area.csv')
df_unemployment = pd.read_csv(r'C:\Users\krzys\Downloads\Unemployment.csv')
df_inflation = pd.read_csv(r'C:\Users\krzys\Downloads\Inflation.csv')


##### Reading UK market (this will be AI training data)

df_UK_Prices = pd.read_excel(r'C:\Users\krzys\Downloads\UK House price index (1).xlsx', sheet_name='Average price')
df_UK_Number_of_Dwellings = pd.read_excel(r'C:\Users\krzys\Downloads\Number_and_density_of_dwellings_by_borough.xlsx', sheet_name='Number of dwellings')
df_UK_Dwellings_per_hectare = pd.read_excel(r'C:\Users\krzys\Downloads\Number_and_density_of_dwellings_by_borough.xlsx', sheet_name='Dwellings per hectare')
df_UK_earnings = pd.read_excel(r'c:\Users\krzys\Downloads\earnings-residence-borough.xlsx', sheet_name='Full-time, Weekly')
df_UK_jobs = pd.read_excel(r'c:\Users\krzys\Downloads\jobs-and-job-density.xlsx', sheet_name='Jobs')
df_UK_population_estimates = pd.read_excel(r'c:\Users\krzys\Downloads\ons-mye-custom-age-tool-2020.xlsx', sheet_name='Single year of age')

##### Cleaning data


print(df_UK_population_estimates.head(20))

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


##### Analysist


## Random Forest



## Neutral network



##### Ploting

i=0
plt.figure(figsize=(8, 6))
for index, row in dataframe.iterrows():
    plt.plot(dataframe.columns, dataframe.iloc[i], marker='o', label=f'Row {index}')
    i = i +1

plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()
