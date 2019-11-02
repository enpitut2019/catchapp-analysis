# Installation
### Python3
バージョン確認
```
$ python3 —verison
```
入ってればよし。入ってなければ以下でinstall
```
$ sudo apt install python3.7
```
でバージョン確認。OSによっては3.7が無いのでその時は3.5

### Pipenv //sudameくん補足して
```
$ pip install pipenv
$ pipenv --python 3    # Python3系で初期化
```

### その他の依存関係 //sudameくん補足して

```
$ pipenv sync
```

これで以下の依存が解決するので、このリポジトリをgit cloneすれば動く。
- pandas
- arxiv
- requests
- googletrans

# Quick start
- 以下の手順でとりあえずの動作試験可能
```
$ cd <catchapp-analysis directory>
$ python3 integration/integration_authors.py
```
- 実行不可能な場合は以下のように自分のpythonのバージョンにあわせて実行(下は3.6を想定)
```
$ python3.6 integration/integration_authors.py
```
- また、Python のファイルには権限付与が必要な場合がある。以下で実行権限付与。
```
$ chmod a+x integration/integration_authors.py
```

# Structure
以下にこのリポジトリのディレクトリ構造を記載
### integration
- 統合されたプログラムが格納
- 依存関係
    - pandas
    - arxiv
    - requests
    - googletrans
### parts
- 個別の機能毎のプログラムが格納
- arxiv
    - arxivからのデータの取得
    - 依存関係
        - pandas
        - arxiv
- translation
    - 翻訳
    - 依存関係
        - googletrans

# Tutorial
これまでに導入されている googletrans, arxiv それぞれの API がどのように使用できるかを以下で学習可能

### Step.1 arXiv
- 概要
    - arXiv は多くの研究論文がアップロードされているインターネット上のデジタルアーカイブ
    - [API](https://arxiv.org/help/api/user-manual) が公開されておりいくつかのスクリプトによって使用可能(今回はPythonから使用)
    - 今回は論文の絞り込みと基本情報取得の2種類の機能を使用
- 単体での実行
    - /parts内にそれぞれの機能ごとのスクリプトがあるためそれを実行すれば単体での試験が可能
    - /parts/arxiv内の`arxiv_api.py`で論文の基本情報取得のみが可能
 ```
$ python3 parts/arxiv/arxiv_api.py
```   
- コードの解説
    - 該当のpythonファイルをエディターで開きながら見て欲しい
    - コードの要点を説明していく
    - まずpythonでは```#```がコメントアウトの役割を持つ
    - ```import```によってプログラムに必要なライブラリをインポートしている今回は以下の3つ
        - pprint
            - ターミナル出力用のライブラリ
        - arxiv
            - arxiv API
        - pandas
            - 計算用ライブラリ
    - 次に arxiv の検索機能について説明する(該当するのは以下の行)
    ```
    l = arxiv.query(query='au:"Grisha Perelman"')
    ```
    - これは"Grisha Perelman"という著者の論文を取得し行列```l```に格納するものである
    - これ移行は行列のインデックスによって論文とその基本情報の種類を指定しアクセスできるようになっている
    - ここでは著者によって検索がかけられているが何によって検索をかけるかを決定づけているのが```au:```の部分これは author の au であり他の要素でも検索は可能
    - 検索可能なのは以下の要素

    |**prefix**|**explanation**|
    |-|-|
    |ti|Title|
    |au|Author|
    |abs|Abstract|
    |co|Comment|
    |jr|Journal Reference|
    |cat|Subject Category|
    |rn|Report Number|
    |id|Id (use `id_list` instead)|
    |all|All of the above|

    - 後は基本情報の取得のみであるがそれは以下のように```l```の要素にアクセスすれば可能
    ```
    print("\ntitle:\n" + l[0]['title'])
    ```
    - ここでは検索結果一本目の論文(インデックス```0```)の```title```の要素にアクセスしている
    - ひとつ目の[]ないの数字で何本目の論文にアクセスするかふたつめでなんの情報にアクセスするかを指定している
    - ```title```以外にも取得できる情報はある(下の表を参照)

    |**element**|**explanation**|
    |-|-|
    |`<title>`|The title of the article.|
    |`<id>`|A url `http://arxiv.org/abs/id`|
    |`<published>`|The date that `version 1` of the article was submitted.|
    |`<updated>`|The date that the retrieved version of the article was submitted. Same as `<published>` if the retrieved version is version 1.|
    |`<summary>`|The article abstract.|
    |`<author>`|One for each author. Has child element `<name>` containing the author name.|
    |`<link>`|Can be up to 3 given url's associated with this article.|
    |`<category>`|The arXiv or ACM or MSC category for an article if present.|
    |`<arxiv:primary_category>`|The primary arXiv category.|
    |`<arxiv:comment>`|The authors comment if present.|
    |`<arxiv:affiliation>`|The author's affiliation included as a subelement of `<author>` if present.|
    |`<arxiv:journal_ref>`|A journal reference if present.|
    |`<arxiv:doi>`|A url for the resolved DOI to an external resource if present.|
    - 以上で`arxiv_api.py`の説明を終わる
