import subprocess
import os
import urllib.request

# URL先のPDFを取得して pdffile.pdf という名前で保存
urllib.request.urlretrieve("https://arxiv.org/pdf/1911.04929", "pdffile.pdf")

# PHPを呼び出して解析
proc = subprocess.Popen(
    "php /app/PDFNLT-1.0-1.0/pdfanalyzer/pdfanalyze.php --with-image --model /app/PDFNLT-1.0-1.0/pdfanalyzer/paper.model -c generate_xhtml /app/callphp/pdffile.pdf", shell=True, stdout=subprocess.PIPE)
# 解析ツールの出力を読み込んでコンソールに出力
print(proc.stdout.read())
