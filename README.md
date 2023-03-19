# paper2slack

APIを使って論文を探して、ChatGPTに要約してもらった文章をSlackのbotに投げてもらうコードです。

ローカルで実行して見たい人は、まず以下で必要なライブラリをインストールします。
```
$ pip install -r requirements.txt
```
その後、以下で実行してください。

arixv論文の場合
```
$ python paper_arxiv.py
```

IEEE論文の場合
```
$ python paper_ieee.py
```

クラウドで実行したい場合は[こちらのサイト](https://gammasoft.jp/blog/schdule-running-python-script-by-serverless/)を参考にしてmain.pyとrequirements.txtを使用してください。
