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
CHECK_INTERVAL = 1800     # 30分間隔（秒）に変更
HISTORY_FILE = "processed_tweets.txt"

# リプライメッセージリスト
REPLIES = [
    "今日も元気ですね！",
    "興味深いツイートありがとう！",
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
        self.target_user_id = self.get_user_id_with_retry()
        self.last_api_call = datetime.now() - timedelta(minutes=30)

    def get_user_id_with_retry(self, retries=3, backoff_factor=2):
        for attempt in range(retries):
            try:
                user = self.client.get_user(username=TARGET_USERNAME)
                return user.data.id
            except tweepy.TweepyException as e:
                if e.response.status_code == 429:
                    wait_time = backoff_factor ** (attempt + 1)
                    print(f"レートリミット検出. {wait_time}秒待機...")
                    time.sleep(wait_time)
                else:
                    print(f"ユーザーID取得エラー: {e}")
                    exit(1)
        print("最大再試行回数に達しました")
        exit(1)

    def load_processed_tweets(self):
        try:
            with open(HISTORY_FILE, "r") as f:
                return set(f.read().splitlines())
        except FileNotFoundError:
            open(HISTORY_FILE, 'w').close()
            return set()

    def save_tweet_id(self, tweet_id):
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{tweet_id}\n")
        self.processed_tweets.add(tweet_id)

    def check_new_tweets(self):
        try:
            current_time = datetime.now()
            if (current_time - self.last_api_call).seconds < CHECK_INTERVAL:
                print("レートリミット回避のためスキップ")
                return

            tweets = self.client.get_users_tweets(
                self.target_user_id,
                exclude=["replies", "retweets"],
                tweet_fields=["created_at"],
                max_results=5
            )

            new_tweets = [
                t for t in tweets.data 
                if t.id not in self.processed_tweets
                and datetime.utcnow() - t.created_at < timedelta(minutes=30)
            ]

            for tweet in reversed(new_tweets):
                self.send_reply(tweet.id)
                self.save_tweet_id(tweet.id)

            self.last_api_call = datetime.now()

        except tweepy.TweepyException as e:
            if e.response.status_code == 429:
                reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
                wait_seconds = max(reset_time - int(time.time()), 300)
                print(f"レートリミット到達. {wait_seconds}秒待機...")
                time.sleep(wait_seconds)
            else:
                print(f"APIエラー: {e}")

    def send_reply(self, tweet_id):
        try:
            auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
            api = tweepy.API(auth, wait_on_rate_limit=True)
            
            reply_text = f"{random.choice(REPLIES)}"
            api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            print(f"リプライ送信: {reply_text}")
            time.sleep(60)  # リプライ間隔を保証

        except Exception as e:
            print(f"リプライ失敗: {e}")

if __name__ == "__main__":
    monitor = TwitterMonitor()
    while True:
        print(f"{datetime.now()} チェック開始...")
        monitor.check_new_tweets()
        sleep_duration = CHECK_INTERVAL - (datetime.now() - monitor.last_api_call).seconds
        if sleep_duration > 0:
            print(f"次のチェックまで{sleep_duration}秒待機")
            time.sleep(sleep_duration)
