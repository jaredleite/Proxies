import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
#from random import choice
from time import sleep


raw_proxies_file = os.getcwd() + '\\raw_proxies.csv'
treated_proxies_file = os.getcwd() + '\\treated_proxies.csv'
link_test_list_file = ''


proxyDict = {
    "http": '1',
            "https": '2'
}

url = 'https://free-proxy-list.net/'


def test():
    global proxyDict
    r = requests.get("http://ipinfo.io/json", timeout=3, proxies=proxyDict)
    print(r.content)
    return r.status_code


def Raw_Proxies():
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

    # print(df.head())
    # print(df.tail())

    df.to_csv(raw_proxies_file, index=False, encoding='utf-8')
    return df


def Main():
    global proxyDict
    good_proxies_list = []

    df_raw_proxies = Raw_Proxies()
    for p in df_raw_proxies['ip']:
        try:
            proxyDict['http'] = p
            proxyDict['https'] = p

            r = test()

            if r == 200:
                good_proxies_list.append(p)
        except:
            print(f'fail/{p}')
    print(good_proxies_list)


Main()
