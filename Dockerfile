FROM ubuntu:16.04
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update \
    && apt-get install -y wget libfontconfig1-dev libjpeg-dev libopenjpeg-dev xfonts-scalable libleptonica-dev liblbfgs-dev unzip mecab-ipadic-utf8 php php-dev libmecab-dev php-pspell aspell aspell-en php-mbstring imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# PDFNLT本体のダウンロードと解凍
RUN wget https://github.com/KMCS-NII/PDFNLT-1.0/archive/v1.0.tar.gz
RUN tar xzvf v1.0.tar.gz

# Popplerのインストール
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist
RUN tar xJf poppler-0.52.0.tar.xz
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/poppler-0.52.0
RUN gzip -dc ../poppler-0.52.0.patch.gz | patch -p1
RUN ./configure --enable-xpdf-headers
RUN make
RUN make install

# libpoppler.so.66 が無いと怒られるので……
RUN cp /usr/local/lib/libpoppler.so.66 /usr/lib/

# pdffiguresのインストール
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist
RUN unzip pdffigures-20160622.zip
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/pdffigures-master
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"
RUN make DEBUG=0
# (インストーラはないので手でコピー)
RUN cp pdffigures /usr/local/bin/

# crfsuite のインストール
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/
RUN tar xvfz crfsuite-0.12.tar.gz
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/crfsuite-0.12
RUN ./configure
RUN make
RUN make install

# MeCab, php-mecab のインストール（オプション）
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/
RUN tar xfz php-mecab-0.6.0.tgz
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/dist/php-mecab/mecab
RUN phpize
RUN ./configure
RUN make
RUN make install
RUN echo "; configuration for php mecab module" >> /etc/php/7.0/cli/conf.d/mecab.ini
RUN echo "; priority=20" >> /etc/php/7.0/cli/conf.d/mecab.ini
RUN echo "extension=mecab.so" >> /etc/php/7.0/cli/conf.d/mecab.ini

# サンプルデータでモデル作成
WORKDIR /app/PDFNLT-1.0-1.0/pdfanalyzer/
RUN tar xfz dist/sampledata.tgz
RUN mv sampledata/* .

# アノテーションデータからトレーニングデータを更新
RUN php pdfanalyze.php --command update_training --all

# トレーニングデータからモデルを更新
RUN cp /usr/local/lib/libcrfsuite-0.12.so /usr/lib/
RUN cp /usr/local/lib/libcqdb-0.12.so /usr/lib/
RUN php pdfanalyze.php --command update_model

# Python 3.7 の環境を構築
# git のインストール
RUN apt-get update \
    && apt-get install -y zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libbz2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tar.xz
RUN tar xf Python-3.7.5.tar.xz
WORKDIR /app/Python-3.7.5
RUN ./configure --with-ensurepip
RUN make
RUN make install
WORKDIR /app

# python, pipコマンドを呼べるようにする
RUN ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip

# pipenvをインストール
RUN pip3 --disable-pip-version-check install pipenv

# 不要になったファイルの削除
RUN rm -rf Python-3.7.5 \
    && rm Python-3.7.5.tar.xz \
    && rm v1.0.tar.gz

# pdfanalyzerの取り出し
WORKDIR /app
RUN mkdir pdfanalyzer \
    && mv PDFNLT-1.0-1.0/pdfanalyzer/pdfanalyze.php ./pdfanalyzer/ \
    && mv PDFNLT-1.0-1.0/pdfanalyzer/lib/ ./pdfanalyzer/ \
    && mv PDFNLT-1.0-1.0/pdfanalyzer/paper.model ./pdfanalyzer/ \
    && rm -rf PDFNLT-1.0-1.0

# git のインストール
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*