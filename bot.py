import os
import random
import time
from datetime import datetime
import tweepy
import logging

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Twitter API v2の認証
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# 監視するアカウントのリスト
target_accounts = ["@_09x"]  # 監視したいアカウントを指定

# リプライのリスト
replies = ["テストリプライです！", "こんにちは！", "いいね！"]

# 1日のツイート数をカウントする変数
daily_tweet_count = 0

def check_tweets():
    global daily_tweet_count
    for account in target_accounts:
        try:
            logging.info(f"ユーザー {account} のツイートをチェック中...")

            # ユーザー情報を取得
            user = client.get_user(username=account.replace("@", ""))
            if not user.data:
                logging.warning(f"ユーザー {account} が見つかりません")
                continue

            # ユーザーの最新ツイートを取得
            tweets = client.get_users_tweets(user.data.id, max_results=1)
            if not tweets.data:
                logging.info(f"{account} のツイートはありません")
                continue

            for tweet in tweets.data:
                logging.info(f"最新ツイート: {tweet.text}")
                if daily_tweet_count < 40:  # 1日のツイート数を40回に制限
                    if "テスト" in tweet.text:  # 条件を追加
                        reply = random.choice(replies)
                        client.create_tweet(text=f"@{account} {reply}", in_reply_to_tweet_id=tweet.id)
                        daily_tweet_count += 1
                        logging.info(f"Replied to {account} with {reply}")
                    else:
                        logging.info(f"条件に合わないツイート: {tweet.text}")
                else:
                    logging.warning("1日のツイート制限に達しました")
        except Exception as e:
            logging.error(f"エラー: {str(e)}")

# 毎日ツイートカウントをリセットする関数
def reset_daily_tweet_count():
    global daily_tweet_count
    daily_tweet_count = 0

# メインループ
if __name__ == "__main__":
    logging.info("Botを開始します...")
    while True:
        try:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:  # 毎日0時にツイートカウントをリセット
                reset_daily_tweet_count()
            check_tweets()
            time.sleep(60)  # 1分ごとにチェック
        except Exception as e:
            logging.error(f"メインループエラー: {str(e)}")
            time.sleep(60)  # エラー時も1分待機
