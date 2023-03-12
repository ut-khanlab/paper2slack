import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import arxiv
import openai
import random

#OpenAIのapiキー
openai.api_key = 'OpenAIのAPIキー'
# Slack APIトークンを環境変数から取得する
SLACK_API_TOKEN = 'SlackbotのAPIトークン'
# Slackに投稿するチャンネル名を指定する
SLACK_CHANNEL = "#general"

def get_summary(result):
    system = """与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。```
    タイトルの日本語訳
    ・要点1
    ・要点2
    ・要点3
    ```"""

    text = f"title: {result.title}\nbody: {result.summary}"
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.25,
            )
    summary = response['choices'][0]['message']['content']
    title_en = result.title
    title, *body = summary.split('\n')
    body = '\n'.join(body)
    date_str = result.published.strftime("%Y-%m-%d %H:%M:%S")
    message = f"発行日: {date_str}\n{result.entry_id}\n{title_en}\n{title}\n{body}\n"
    
    return message

# Slack APIクライアントを初期化する
client = WebClient(token=SLACK_API_TOKEN)
#queryを用意、今回は、三種類のqueryを用意
query_1 ='ti:%22 Anomaly Detection %22 OR ti:%22 Fault Detection %22 OR ti:%22 Fault Diagnosis %22'
query_2 ='ti:%22 Model Predictive Control %22 OR %22 Fault Tolerant Control %22'
query_3 = 'ti:Spacecraft OR ti:On-board OR ti:%22 Aerospace Engineering %22'
query_list = [query_1, query_2, query_3]

# arxiv APIで最新の論文情報を取得する
for i, query in enumerate(query_list):
    search = arxiv.Search(
        query=query,  # 検索クエリ（
        max_results=300,  # 取得する論文数
        sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
        sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
    )
    #searchの結果をリストに格納
    result_list = []
    for result in search.results():
        result_list.append(result)
    #ランダムにnum_papersの数だけ選ぶ
    num_papers = 1
    results = random.sample(result_list, k=num_papers)
    
    # 論文情報をSlackに投稿する
    for result in results:
        try:
            # Slackに投稿するメッセージを組み立てる
            message = "今日の論文です！ " + str(i+1) + "本目\n" + get_summary(result)
            # Slackにメッセージを投稿する
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=message
            )
            print(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            print(f"Error posting message: {e}")