import xml.etree.ElementTree as ET
import re
import arxiv
import urllib.request
import subprocess
import os
import json
import requests as http
from googletrans import Translator
translator = Translator()

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


# arxivの使い方は宋さんやOEIさんあたりのを参考に脳死で書いた
paper_list = arxiv.query(query='cat:"cs.AI"', max_results=30)

print(len(paper_list))

for paper in paper_list:
    # PDFファイルを保存
    response = urllib.request.urlretrieve(
        paper['pdf_url'], 'paper.pdf',)

    # Paperの基本データをRailsにPOSTする
    # paper_create_url = 'http://host.docker.internal:3000/papers/create'
    paper_create_url = 'https://siscorn-checkapp.herokuapp.com/papers/create'
    summary = paper["summary"].replace('\n', ' ')
    title = paper["title"].replace('\n', ' ')
    data = {
        "abstract": summary,
        "title": title,
        "url": paper["arxiv_url"],
        "abstract_ja": translator.translate(summary, src='en', dest='ja').text,
        "pdf_url": paper["pdf_url"],
        "published_at": paper["published"],
        "journal": "",
        "title_ja": translator.translate(title, src='en', dest='ja').text,
        "cite_count": "",
        "cited_count": "",
        "authors": ','.join(paper["authors"]),
    }
    print(data)
    res = http.post(paper_create_url, data=data)

    # POSTのレスポンスから保存されたPaperのRails上でのIDを取得する
    paper_id = res.json()['id']

    # PDFNLTを用いて解析
    # 解析結果は xhtml ディレクトリに保存される
    proc = subprocess.run(
        'php /app/pdfanalyzer/pdfanalyze.php --with-image --model /app/pdfanalyzer/paper.model -c generate_xhtml ' + os.getcwd() + '/paper.pdf', shell=True)

    # PDFNLTで生成されたxhtmlファイルを解析する

    # 画像についての解析
    figures = parse_figure(
        ET.parse("./xhtml/paper.xhtml").getroot(), 'Figure')['figures']
    for figure in figures:
        # 画像のアップロード
        figure_path = './xhtml/' + figure['src']
        # figure_upload_url = 'http://host.docker.internal:3000/papers/upload'
        figure_upload_url = 'https://siscorn-checkapp.herokuapp.com/papers/upload'
        files = {'figure': open(figure_path, 'rb')}
        r = http.post(figure_upload_url, files=files, data={
            'explanation': figure['caption'],
            'paper_id': paper_id,
        })

    # テーブルについての解析
    figures = parse_figure(
        ET.parse("./xhtml/paper.xhtml").getroot(), 'Table')['figures']
    for figure in figures:
        # テーブルの画像のアップロード
        figure_path = './xhtml/' + figure['src']
        # figure_upload_url = 'http://host.docker.internal:3000/papers/upload'
        figure_upload_url = 'https://siscorn-checkapp.herokuapp.com/papers/upload'
        files = {'figure': open(figure_path, 'rb')}
        r = http.post(figure_upload_url, files=files, data={
            'explanation': figure['caption'],
            'paper_id': paper_id,
        })
