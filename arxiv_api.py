import pprint

import requests
import arxiv
import pandas as pd

l = arxiv.query(query='au:"Grisha Perelman"')

#print(type(l))


#print(type(l[0]))


#pprint.pprint(l[0], width=200)

print("author:" + l[0]['author'])

print("title:" + l[0]['title'])

print("arxiv_url:" + l[0]['arxiv_url'])

print("pdf_url:" + l[0]['pdf_url'])

print("summary:" + l[0]['summary'])

response = requests.post("http://localhost:3000/paper/create/")
print(response.status_code)
print(response.text)
