import os
import tweepy

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")  # Bearer Token

# Twitter API v1.1の認証（ユーザー情報取得用）
auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secret,
    access_token,
    access_token_secret
)
api = tweepy.API(auth)

# ストリームリスナーの定義
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"新しいツイート: {tweet.text}")

# ユーザーIDを取得
try:
    user = api.get_user(screen_name="@_09x")  # 監視したいユーザー名を指定
    user_id = user.id_str
    print(f"ユーザーID: {user_id}")
except Exception as e:
    print(f"ユーザーID取得エラー: {str(e)}")
    exit(1)

# ストリームの開始
try:
    stream = MyStreamListener(bearer_token=bearer_token)
    stream.filter(follow=[user_id])  # ユーザーIDを指定
except Exception as e:
    print(f"ストリームエラー: {str(e)}")
