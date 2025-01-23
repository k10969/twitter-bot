import tweepy
import random
import time
from datetime import datetime
import os

# Twitter APIの認証
auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"),
    os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

# 監視するアカウントのリスト
target_accounts = ["@_09x", "@account2"]  # ここに監視したいアカウントを入力

# リプライのリスト
replies = ["Reply 1", "Reply 2", "Reply 3"]  # ここにリプライ内容を入力

# 1日のツイート数をカウントする変数
daily_tweet_count = 0

def check_tweets():
    global daily_tweet_count
    for account in target_accounts:
        tweets = api.user_timeline(screen_name=account, count=1, tweet_mode="extended")
        for tweet in tweets:
            if not tweet.retweeted and not tweet.favorited:
                if daily_tweet_count < 40:  # 1日のツイート数を40回に制限
                    reply = random.choice(replies)
                    api.update_status(f"@{tweet.user.screen_name} {reply}", in_reply_to_status_id=tweet.id)
                    daily_tweet_count += 1
                    print(f"Replied to {tweet.user.screen_name} with {reply}")
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
