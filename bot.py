import os
import tweepy

# APIキーの取得
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# ストリームリスナーの定義
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"新しいツイート: {tweet.text}")

# ストリームの開始
try:
    # ストリームリスナーのインスタンスを作成
    stream = MyStreamListener(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN")  # Bearer Tokenが必要
    )

    # 監視するユーザーのIDを指定
    user = api.get_user(screen_name="@_09x")  # 監視したいユーザー名を指定
    user_id = user.id_str
    print(f"ユーザーID: {user_id}")

stream.filter(follow=[user_id])  # ユーザーIDを指定
