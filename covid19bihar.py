import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd


URL = 'https://www.mohfw.gov.in/'
  
HEADERS = ['S No.', 'State','Total Confirmed Cases','Discharged','Death'] 
  
response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 

remove_newl_char = lambda row: [x.text.replace('\n', '') for x in row] 

all_rows = soup.find_all('tr') 
df = pd.DataFrame(columns = HEADERS) 
for row in all_rows: 
    data = remove_newl_char(row.find_all('td')) 
    if data:
        if len(data)==5:
            df.loc[len(df)] = data
for j in ['S No.', 'Total Confirmed Cases','Discharged','Death']:
    df[j] = pd.to_numeric(df[j])
df.loc[len(df)] = [df.iloc[len(df)-1,0]+1,'INDIA',df['Total Confirmed Cases'].sum(),df['Discharged'].sum(),df['Death'].sum()]
df = df.set_index('S No.')
df = df.sort_values('Total Confirmed Cases')
print(df)

plt.barh( list(df['State']),list(df['Total Confirmed Cases']), align='center', alpha=0.5, 
                 color=(234/256.0, 128/256.0, 252/256.0), 
                 edgecolor=(106/256.0, 27/256.0, 154/256.0)
                 ,height = 0.5) 
  
plt.yticks(list(df['State']),  list(df['State'])) 
plt.xlim(1,500) 
plt.xlabel('Number of Cases') 
plt.title('Corona Virus Cases') 
plt.show() 

response = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml#').content 
soup = BeautifulSoup(response, 'html.parser') 