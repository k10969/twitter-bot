import os
import random
import time
from datetime import datetime
import tweepy

# 環境変数の確認
print("=== Environment Variables Check ===")
for env_var in ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]:
    value = os.getenv(env_var)
    if value:
        print(f"{env_var}: ✓ (設定されています)")
        print(f"Length: {len(value)} characters")
    else:
        print(f"{env_var}: ✗ (未設定です)")

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

if not all([api_key, api_secret, access_token, access_token_secret]):
    print("エラー: 必要な環境変数が設定されていません")
    exit(1)

# Twitter API v2の認証
try:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    print("Twitter API v2認証成功!")
except Exception as e:
    print(f"Twitter API認証エラー: {str(e)}")
    exit(1)

# 監視するアカウントのリスト
target_accounts = ["@_09x", "@account2"]  # ここに監視したいアカウントを入力

# リプライのリスト
replies = ["テストだよ", "Reply 2", "Reply 3"]  # ここにリプライ内容を入力

# 1日のツイート数をカウントする変数
daily_tweet_count = 0

def check_tweets():
    global daily_tweet_count
    for account in target_accounts:
        try:
            # ユーザーの最新ツイートを取得
            user = client.get_user(username=account)
            tweets = client.get_users_tweets(user.data.id, max_results=1)
            for tweet in tweets.data:
                if daily_tweet_count < 40:  # 1日のツイート数を40回に制限
                    reply = random.choice(replies)
                    client.create_tweet(text=f"@{account} {reply}", in_reply_to_tweet_id=tweet.id)
                    daily_tweet_count += 1
                    print(f"Replied to {account} with {reply}")
                else:
                    print("Daily tweet limit reached.")
        except Exception as e:
            print(f"Error processing tweets for {account}: {str(e)}")

# 毎日ツイートカウントをリセットする関数
def reset_daily_tweet_count():
    global daily_tweet_count
    daily_tweet_count = 0

# メインループ
if __name__ == "__main__":
    print("Bot starting...")
    while True:
        try:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:  # 毎日0時にツイートカウントをリセット
                reset_daily_tweet_count()
            check_tweets()
            time.sleep(60)  # 1分ごとにチェック
        except Exception as e:
            print(f"Main loop error: {str(e)}")
            time.sleep(60)  # エラー時も1分待機
