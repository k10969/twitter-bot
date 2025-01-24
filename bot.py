import os
import time
import tweepy

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")  # Bearer Token

# Twitter API v2の認証
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# ユーザー情報を取得
try:
    username = "@_09x"  # 監視したいユーザー名
    username_cleaned = username.replace("@", "")  # @ を除去
    user = client.get_user(username=username_cleaned)  # クリーンなユーザー名を使用
    if user.data:
        user_id = user.data.id
        print(f"ユーザーID: {user_id}")
    else:
        print("ユーザーが見つかりません")
except tweepy.TooManyRequests as e:
    print(f"レートリミットに達しました: {str(e)}")
    reset_time = int(e.response.headers.get("x-rate-limit-reset"))  # リセット時刻を取得
    sleep_time = reset_time - int(time.time())  # リセットまでの待機時間を計算
    print(f"リセットまで {sleep_time} 秒待機します...")
    time.sleep(sleep_time)  # リセットまで待機
except Exception as e:
    print(f"ユーザー情報取得エラー: {str(e)}")
