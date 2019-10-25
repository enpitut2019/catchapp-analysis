import pprint

import requests
import arxiv
import pandas as pd

l = arxiv.query(query='au:"Grisha Perelman"')

#print(type(l))




#print(type(l[0]))


#pprint.pprint(l[0], width=200)
# {'affiliation': 'None',
#  'arxiv_comment': '39 pages',
#  'arxiv_primary_category': {'scheme': 'http://arxiv.org/schemas/atom', 'term': 'math.DG'},
#  'arxiv_url': 'http://arxiv.org/abs/math/0211159v1',
#  'author': 'Grisha Perelman',
#  'author_detail': {'name': 'Grisha Perelman'},
#  'authors': ['Grisha Perelman'],
#  'doi': None,
#  'guidislink': True,
#  'id': 'http://arxiv.org/abs/math/0211159v1',
#  'journal_reference': None,
#  'links': [{'href': 'http://arxiv.org/abs/math/0211159v1', 'rel': 'alternate', 'type': 'text/html'},
#            {'href': 'http://arxiv.org/pdf/math/0211159v1', 'rel': 'related', 'title': 'pdf', 'type': 'application/pdf'}],
#  'pdf_url': 'http://arxiv.org/pdf/math/0211159v1',
#  'published': '2002-11-11T16:11:49Z',
#  'published_parsed': time.struct_time(tm_year=2002, tm_mon=11, tm_mday=11, tm_hour=16, tm_min=11, tm_sec=49, tm_wday=0, tm_yday=315, tm_isdst=0),
#  'summary': 'We present a monotonic expression for the Ricci flow, valid in all dimensions\n'
#             'and without curvature assumptions. It is interpreted as an entropy for a\n'
#             'certain canonical ensemble. Several geometric applications are given. In\n'
#             'particular, (1) Ricci flow, considered on the space of riemannian metrics\n'
#             'modulo diffeomorphism and scaling, has no nontrivial periodic orbits (that is,\n'
#             'other than fixed points); (2) In a region, where singularity is forming in\n'
#             'finite time, the injectivity radius is controlled by the curvature; (3) Ricci\n'
#             'flow can not quickly turn an almost euclidean region into a very curved one, no\n'
#             'matter what happens far away. We also verify several assertions related to\n'
#             "Richard Hamilton's program for the proof of Thurston geometrization conjecture\n"
#             'for closed three-manifolds, and give a sketch of an eclectic proof of this\n'
#             'conjecture, making use of earlier results on collapsing with local lower\n'
#             'curvature bound.',
#  'summary_detail': {'base': 'http://export.arxiv.org/api/query?search_query=au%3A%22Grisha+Perelman%22&id_list=&start=0&max_results=1000&sortBy=relevance&sortOrder=descending',
#                     'language': None,
#                     'type': 'text/plain',
#                     'value': 'We present a monotonic expression for the Ricci flow, valid in all dimensions\n'
#                              'and without curvature assumptions. It is interpreted as an entropy for a\n'
#                              'certain canonical ensemble. Several geometric applications are given. In\n'
#                              'particular, (1) Ricci flow, considered on the space of riemannian metrics\n'
#                              'modulo diffeomorphism and scaling, has no nontrivial periodic orbits (that is,\n'
#                              'other than fixed points); (2) In a region, where singularity is forming in\n'
#                              'finite time, the injectivity radius is controlled by the curvature; (3) Ricci\n'
#                              'flow can not quickly turn an almost euclidean region into a very curved one, no\n'
#                              'matter what happens far away. We also verify several assertions related to\n'
#                              "Richard Hamilton's program for the proof of Thurston geometrization conjecture\n"
#                              'for closed three-manifolds, and give a sketch of an eclectic proof of this\n'
#                              'conjecture, making use of earlier results on collapsing with local lower\n'
#                              'curvature bound.'},
#  'tags': [{'label': None, 'scheme': 'http://arxiv.org/schemas/atom', 'term': 'math.DG'}, {'label': None, 'scheme': 'http://arxiv.org/schemas/atom', 'term': '53C'}],
#  'title': 'The entropy formula for the Ricci flow and its geometric applications',
#  'title_detail': {'base': 'http://export.arxiv.org/api/query?search_query=au%3A%22Grisha+Perelman%22&id_list=&start=0&max_results=1000&sortBy=relevance&sortOrder=descending',
#                   'language': None,
#                   'type': 'text/plain',
#                   'value': 'The entropy formula for the Ricci flow and its geometric applications'},
#  'updated': '2002-11-11T16:11:49Z',
#  'updated_parsed': time.struct_time(tm_year=2002, tm_mon=11, tm_mday=11, tm_hour=16, tm_min=11, tm_sec=49, tm_wday=0, tm_yday=315, tm_isdst=0)}

print(l[0]['author'])

print(l[0]['title'])

print(l[0]['arxiv_url'])

print(l[0]['pdf_url'])

print(l[0]['summary'])

#pprint.pprint([a['id'] for a in l])
# ['http://arxiv.org/abs/math/0211159v1',
#  'http://arxiv.org/abs/math/0303109v1',
#  'http://arxiv.org/abs/math/0307245v1']

pprint.pprint( a['published'] for a in l)
# [['http://arxiv.org/abs/math/0211159v1', '2002-11-11T16:11:49Z'],
#  ['http://arxiv.org/abs/math/0303109v1', '2003-03-10T16:44:35Z'],
#  ['http://arxiv.org/abs/math/0307245v1', '2003-07-17T15:26:38Z']]

#df = pd.io.json.json_normalize(l)
#print(df.shape)


#print(df[['title', 'published']])
#                                                title             published
# 0  The entropy formula for the Ricci flow and its...  2002-11-11T16:11:49Z
# 1         Ricci flow with surgery on three-manifolds  2003-03-10T16:44:35Z
# 2  Finite extinction time for the solutions to th...  2003-07-17T15:26:38Z

l = arxiv.query(query='cat:cs.AI', max_results=10, sort_by='submittedDate')

#pprint.pprint([[a['id'], a['published']] for a in l])


#response = requests.post("http://localhost:3000/paper/create/")
# print(response.status_code)
# print(response.text)
