#!/usr/bin/env python
import pprint

# import requests
import arxiv
import pandas as pd

from googletrans import Translator
translator = Translator()

# p_list = arxiv.query(query='au:"Grisha Perelman"')
p_list = arxiv.query(query='au:"Henggang Cui"')


# num = len(p_list)

# print(type(l))


# print(type(l[0]))


#pprint.pprint(l[0], width=200)

for i in p_list:
    print("\n\n\n----------------------------------------------------------------------------------------------------")
    print("\nタイトル:\n" + translator.translate(i['title'],
                                             src='en', dest='ja').text + '\n(' + i['title'] + ')')
    print("\npublished:\n" + i['published'])
    print("\nauthors:")
    for j in i['authors']:
        print(j + ",", end="")
    # print("\n")
    print("\n\nterm:\n" + i['arxiv_primary_category']['term'])
    print("\narxiv_url:\n" + i['arxiv_url'])
    print("\npdf_url:\n" + i['pdf_url'])
    print("\nsummary:\n" + i['summary'])
    print("\n要約:\n" +
          translator.translate(i['summary'], src='en', dest='ja').text)


#response = requests.post("http://localhost:3000/paper/create/")
# print(response.status_code)
# print(response.text)
