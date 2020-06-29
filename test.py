from threading import *
import time
import requests
import json
import pprint
l = []
Paytm_URL = "https://search.paytm.com/v2/search?userQuery=Micromax+TV&page_count=5&items_per_page=30"
Shopclues_URL = "http://api.shopclues.com/api/v11/search?q=Micromax+TV&z=1&key=d12121c70dda5edfgd1df6633fdb36c0&page=2"
TataCliq_URL = "https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/serpsearch?type=category&channel=mobile&pageSize=20&typeID=al&page=0&searchText=Micromax+TV&isFilter=false&isTextSearch=true"
def firstfunc():
    result = []
    i = 0
    while i <= 100:
        result = requests.get(f'https://search.paytm.com/v2/search?userQuery=Micromax+TV&page_count={i}&items_per_page=30')
        if result != None:
            for key,val in result.json().items():
                if isinstance(val,dict):
                    l.append(val)
        i= i+1

def secondfunc():
    result = []
    i = 0
    while i <= 100:
        result = requests.get(f"http://api.shopclues.com/api/v11/search?q=Micromax+TV&z=1&key=d12121c70dda5edfgd1df6633fdb36c0&page={i}")
        if result != None:
            for key,val in result.json().items():
                if isinstance(val,dict):
                    l.append(val)
        i= i+1

def thirdfunc():
    result = []
    i = 0
    while i != 100:
        result = requests.get(f"https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/serpsearch?type=category&channel=mobile&pageSize=20&typeID=al&page={i}&searchText=Micromax+TV&isFilter=false&isTextSearch=true")
        if result != None:
            for key,val in result.json().items():
                if isinstance(val,dict):
                    l.append(val)
        i= i+1
t1 = Thread(target=firstfunc)
t2 = Thread(target=secondfunc)
t3 = Thread(target=thirdfunc)
t1.start()
t2.start()
t3.start()
time.sleep(2)
k = l.copy()
pprint.pprint(k[10])
# time.sleep(6)
# print(l)
# style="border:1px solid green;width:70%;padding-top:5%"
