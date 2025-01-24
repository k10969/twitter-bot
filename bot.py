import os
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
except Exception as e:
    print(f"ユーザー情報取得エラー: {str(e)}")
