#import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
#from random import choice
from time import sleep

url = 'https://free-proxy-list.net/'
r = requests.get(url, timeout=4)
sleep(5)
soup = BeautifulSoup(r.content, 'html.parser')

rows = soup.find_all('tr')

ip = []
country = []
https = []

for rw in rows:
    try:
        cols = rw.find_all('td')
        ip_adrress = cols[0].get_text()
        port = cols[1].get_text()
        country_name = cols[3].get_text()
        https_YorN = cols[6].get_text()
        if ip_adrress.count('.') == 3:
            ip.append(f'{ip_adrress}:{port}')
            country.append(country_name)
            https.append(https_YorN)
    except:
        pass

df = pd.DataFrame(list(zip(ip, country, https)),
                  columns=['ip', 'country', 'https'])

print(df.head())
print(df.tail())
