import os
import requests
import random
import time
from datetime import datetime

# Twitter API v2のエンドポイント
TWITTER_API_URL = "https://api.twitter.com/2/users/{}/tweets"

# Bearer Tokenの設定
BEARER_TOKEN = os.getenv("AAAAAAAAAAAAAAAAAAAAABCBtgEAAAAA4SNS70TjAzp0p5saCM6uDZtBDB0%3DDwBMQ5bxpL8M5bu5nXtVMW10o6svd7qaRaTT42gmlO8CRYHVTP")

# 監視するアカウントのIDリスト
target_user_ids = ["1285420694", "ユーザーID2"]  # ここに監視したいユーザーIDを入力

# リプライのリスト
replies = ["Reply 1", "Reply 2", "Reply 3"]

# 1日のツイート数をカウントする変数
daily_tweet_count = 0

def get_user_tweets(user_id):
    """ユーザーのツイートを取得する関数"""
    url = TWITTER_API_URL.format(user_id)
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def check_tweets():
    global daily_tweet_count
    for user_id in target_user_ids:
        tweets_data = get_user_tweets(user_id)
        if tweets_data and "data" in tweets_data:
            latest_tweet = tweets_data["data"][0]  # 最新のツイートを取得
            tweet_id = latest_tweet["id"]
            tweet_text = latest_tweet["text"]
            print(f"Latest tweet from {user_id}: {tweet_text}")

            # ここにリプライを送信する処理を追加
            if daily_tweet_count < 40:  # 1日のツイート数を40回に制限
                reply = random.choice(replies)
                # リプライを送信する処理（API v2のエンドポイントを使用）
                print(f"Replying to {user_id} with: {reply}")
                daily_tweet_count += 1
            else:
                print("Daily tweet limit reached.")

# 毎日ツイートカウントをリセットする関数
def reset_daily_tweet_count():
    global daily_tweet_count
    daily_tweet_count = 0

# メインループ
if __name__ == "__main__":
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:  # 毎日0時にツイートカウントをリセット
            reset_daily_tweet_count()
        check_tweets()
        time.sleep(60)  # 1分ごとにチェック
