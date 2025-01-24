import os
import tweepy

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Twitter API v1.1の認証
auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secret,
    access_token,
    access_token_secret
)
api = tweepy.API(auth)

# ストリームリスナーの定義
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        print(f"新しいツイート: {status.text}")

# ストリームの開始
try:
    stream = MyStreamListener(
        api_key,
        api_secret,
        access_token,
        access_token_secret
    )
    stream.filter(follow=["ユーザーID"])  # 監視したいユーザーのIDを指定
except Exception as e:
    print(f"ストリームエラー: {str(e)}")
