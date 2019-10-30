#!/usr/bin/env python
import pprint

import requests
import arxiv
import pandas as pd

p_list = arxiv.query(query='au:"Grisha Perelman"')

num = len(p_list)

#print(type(l))


#print(type(l[0]))


#pprint.pprint(l[0], width=200)

for i in p_list:
    
    print("The no." + str(num) + "paper")
    print("\nauthor:\n" + i['author'])
    print("\ntitle:\n" + i['title'])
    print("\narxiv_url:\n" + i['arxiv_url'])
    print("\npdf_url:\n" + i['pdf_url'])
    print("\nsummary:\n" + i['summary'])

#response = requests.post("http://localhost:3000/paper/create/")
#print(response.status_code)
#print(response.text)
