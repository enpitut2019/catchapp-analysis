#!/usr/bin/env python
import pprint

import arxiv
import pandas as pd

from googletrans import Translator
translator = Translator()

l = arxiv.query(query='au:"Grisha Perelman"')

#print(type(l))


#print(type(l[0]))


#pprint.pprint(l[0], width=200)

print("\n著者:\n" + l[0]['author'])

print("\nタイトル:\n" + translator.translate(l[0]['title'], src='en', dest='ja').text + '\n(' + l[0]['title'] + ')')

print("\n要約:\n" + translator.translate(l[0]['summary'], src='en', dest='ja').text)

print("\n要約の原文:\n" + l[0]['summary'])

print("\narxiv_url:\n" + l[0]['arxiv_url'])

print("\npdf_url:\n" + l[0]['pdf_url'])
