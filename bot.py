import os
import tweepy
import random
import time
from datetime import datetime, timedelta

# 環境変数から認証情報を取得
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")

# 監視設定
TARGET_USERNAME = "_09x"  # 監視対象のユーザー名
CHECK_INTERVAL = 900      # 15分間隔（秒）
HISTORY_FILE = "processed_tweets.txt"

# リプライメッセージリスト
REPLIES = [
    "今日も元気ですね！",
    "面白いツイートありがとう！",
    "興味深い内容ですね！",
    "参考になります！",
    "素敵な情報をシェアしてくれて感謝です！"
]

class TwitterMonitor:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET
        )
        self.processed_tweets = self.load_processed_tweets()
        self.target_user_id = self.get_user_id()

    def get_user_id(self):
        try:
            user = self.client.get_user(username=TARGET_USERNAME)
            return user.data.id
        except Exception as e:
            print(f"ユーザーID取得エラー: {e}")
            exit(1)

    def load_processed_tweets(self):
        try:
            with open(HISTORY_FILE, "r") as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            return set()

    def save_tweet_id(self, tweet_id):
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{tweet_id}\n")
        self.processed_tweets.add(tweet_id)

    def check_new_tweets(self):
        try:
            tweets = self.client.get_users_tweets(
                self.target_user_id,
                exclude=["replies", "retweets"],
                tweet_fields=["created_at"],
                max_results=5
            )

            new_tweets = [
                t for t in tweets.data 
                if t.id not in self.processed_tweets
                and datetime.utcnow() - t.created_at < timedelta(minutes=20)
            ]

            for tweet in reversed(new_tweets):
                self.send_reply(tweet.id)
                self.save_tweet_id(tweet.id)

        except tweepy.TweepyException as e:
            print(f"APIエラー: {e}")

    def send_reply(self, tweet_id):
        try:
            auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
            api = tweepy.API(auth)
            
            reply_text = f"{random.choice(REPLIES)}"
            api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            print(f"リプライ送信: {reply_text}")
            time.sleep(60)  # レートリミット回避

        except Exception as e:
            print(f"リプライ失敗: {e}")

if __name__ == "__main__":
    monitor = TwitterMonitor()
    while True:
        print(f"{datetime.now()} チェック開始...")
        monitor.check_new_tweets()
        time.sleep(CHECK_INTERVAL)
