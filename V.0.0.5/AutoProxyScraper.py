import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import sys
import multiprocessing as mp


url = 'https://free-proxy-list.net/'
response = requests.get(url)

FILEPATH = os.path.abspath(__file__)
FILEDIR = FILEPATH.replace(os.path.basename(FILEPATH),'')
z = open(FILEDIR + 'PROXIES.txt','w')
z.close()

soup = BeautifulSoup(response.text, "html.parser")


tr = soup.findAll('tr')

a_proxy = []

types = ['elite proxy','anonymous']
for i in list(tr):
    for typ in types:
        if typ in str(i) and '"hx">yes' in str(i):

            text = str(i)
            text = text.replace('<td','')
            text = text.replace('</td','')
            text = text.replace('<tr>','')
            text = text.replace('</tr>','')
            text = text.replace('>>','>')
            text = text.replace(' ','')

            text = text.split('>')
            text.pop(0)

            text = 'http://' + text[0] +':' +text[1]
            a_proxy.append(text)

z = open(FILEDIR + 'PROXIES.txt','r').read().split('\n')
for i in z:
    a_proxy.append(i)

def remdupe(lis):
        final = []
        seen = []
        for i in lis:
            if i not in seen:
                final.append(i)
                seen.append(i)
        return final

a_proxy = remdupe(a_proxy)
print('Testing %s Proxies..'%(len(a_proxy)))


jobs = []


for proxy in a_proxy:
    def task():
        proxies = {'http':proxy,'https':proxy}
        try:
            for i in range(3):
                r = requests.get('http://effbot.org',proxies=proxies,timeout=1.5)
            z = open(FILEDIR + 'PROXIES.txt','a')
            z.write('\n'+proxy)
            z.close()
            print('%s--- success'%(proxy))
        except:

            print('%s--- failed'%(proxy))

    process = mp.Process(target=task)
    
    try:
        process.start()
    except OSError:
        continue
    jobs.append(process)

for job in jobs:
    if job != None:
        job.join()


       
