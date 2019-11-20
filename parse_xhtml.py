import xml.etree.ElementTree as ET
import re
import arxiv
import urllib.request
import subprocess
import os
import json
import requests as http

### Figure の処理 ###


def parse_figure(root, figure_type):
    result = dict()
    # data-name=Figure なエレメントをすべて取得
    figureElements = root.findall(".//*[@data-name='" + figure_type + "']")

    # Figureを一つ以上含む場合figuresプロパティを生やす
    if len(figureElements) > 0 and not 'figures' in result:
        result['figures'] = []

    # Figure それぞれの処理
    for figure_element in figureElements:
        # Figure IDの取得
        datafig_element = figure_element.find('.//*[@data-fig]')
        if datafig_element != None:
            figure_id = datafig_element.attrib['data-fig']
            img_element = figure_element.find(
                './/{http://www.w3.org/1999/xhtml}img')
            caption_element = root.find(
                './/*[@data-name="Caption"]//*[@data-fig="' + figure_id + '"]')
            if img_element != None and caption_element != None:
                result['figures'].append({
                    'id': figure_id,
                    # Figure 本体の取得
                    'src': img_element.attrib['src'],
                    # Figure キャプションの取得
                    'caption': re.sub(r"\s+", " ", caption_element.text)
                })
    return result


paper_list = arxiv.query(query='au:"Henggang Cui"')

for paper in paper_list:
    response = urllib.request.urlretrieve(
        paper['pdf_url'], 'paper.pdf',)

    proc = subprocess.run(
        'php /app/pdfanalyzer/pdfanalyze.php --with-image --model /app/pdfanalyzer/paper.model -c generate_xhtml ' + os.getcwd() + '/paper.pdf', shell=True)

    res = http.post('http://host.docker.internal:3000/papers/create', data={
        "abstract": paper["summary"],
        "title": paper["title"],
        "url": paper["arxiv_url"],
        "abstract_ja": "",
        "pdf_url": paper["pdf_url"],
        "published_at": paper["published"],
        "journal": "",
        "title_ja": "",
        "cite_count": "",
        "cited_count": "",
        "authors": paper["authors"],
    })

    paper_id = res.json()['id']

    tree = ET.parse("./xhtml/paper.xhtml")
    root = tree.getroot()

    figures = parse_figure(root, 'Figure')['figures']

    for figure in figures:
        figure_path = './xhtml/' + figure['src']
        figure_upload_url = 'http://host.docker.internal:3000/papers/upload'
        files = {'figure': open(figure_path, 'rb')}
        r = http.post(figure_upload_url, files=files, data={
            'explanation': figure['caption'],
            'paper_id': paper_id,
        })

    # print(result)
