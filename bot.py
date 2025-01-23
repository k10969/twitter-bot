from flask import Flask
import os
import requests
import random
import time
from datetime import datetime

app = Flask(__name__)

# Twitter API v2のエンドポイント
TWITTER_API_URL = "https://api.twitter.com/2/users/{}/tweets"

# Bearer Tokenの設定
BEARER_TOKEN = os.getenv("AAAAAAAAAAAAAAAAAAAAAGO8yQEAAAAATeaAbfQ2sZWKyScVhZHPOVh31is%3DhHlxPmVKlyDuRDW9JgeLzPV3IR8ZcjdYRwA1gmQXDIz7sdvT0y")

# 監視するアカウントのIDリスト
target_user_ids = ["44196397"]  # ここに監視したいユーザーIDを入力

# リプライのリスト
replies = ["テストおおお", "Reply 2", "Reply 3"]

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

@app.route('/')
def home():
    return "Twitter Bot is running!"

if __name__ == "__main__":
    # Flaskアプリを起動
    app.run(host='0.0.0.0', port=10000)
