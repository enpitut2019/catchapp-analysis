import xml.etree.ElementTree as ET
import re
import arxiv
import urllib.request
import subprocess
import os
import json
import requests as http
from googletrans import Translator
from bottle import route, run, request, HTTPResponse
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


def parse_xhtml(paper_id, paper_pdf_url):
    # arxivの使い方は宋さんやOEIさんあたりのを参考に脳死で書いた
    figure_upload_url = 'https://catchapp.sudame.net/papers/upload'

    response = urllib.request.urlretrieve(paper_pdf_url, 'paper.pdf',)

    # PDFNLTを用いて解析
    # 解析結果は xhtml ディレクトリに保存される
    proc = subprocess.run(
        'php /app/pdfanalyzer/pdfanalyze.php --with-image --model /app/pdfanalyzer/paper.model -c generate_xhtml ' + os.getcwd() + '/paper.pdf', shell=True)

    # PDFNLTで生成されたxhtmlファイルを解析する

    # 画像についての解析
    figures_raw = parse_figure(
        ET.parse("./xhtml/paper.xhtml").getroot(), 'Figure')
    if 'figures' in figures_raw:
        figures = figures_raw['figures']
        for figure in figures:
            # 画像のアップロード
            figure_path = './xhtml/' + figure['src']
            files = {'figure': open(figure_path, 'rb')}
            r = http.post(figure_upload_url, files=files, data={
                'explanation': figure['caption'],
                'paper_id': paper_id,
            })

    # テーブルについての解析
    figures_raw = parse_figure(
        ET.parse("./xhtml/paper.xhtml").getroot(), 'Table')
    if 'figures' in figures_raw:
        figures = figures_raw['figures']
        for figure in figures:
            # テーブルの画像のアップロード
            figure_path = './xhtml/' + figure['src']
            files = {'figure': open(figure_path, 'rb')}
            r = http.post(figure_upload_url, files=files, data={
                'explanation': figure['caption'],
                'paper_id': paper_id,
            })


def server():
    @route('/')
    def hello():  # pylint: disable=unused-variable
        paper_id = str(request.params.paper_id)  # pylint: disable=no-member
        paper_pdf_url = str(
            request.params.paper_pdf_url)  # pylint: disable=no-member

        response = HTTPResponse(status=200)
        if (not paper_id) or (not paper_pdf_url):
            response.status = 400
        response.body = {
            'status': response.status
        }
        parse_xhtml(paper_id, paper_pdf_url)

        return response
    
    port = os.getenv('PORT', 8080)
    run(host='0.0.0.0', port=port, debug=True)


# launch server
server()
