import os
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

# テストツイートを投稿
try:
    tweet_text = "これはテストツイートです。API v2を使用しています。"
    response = client.create_tweet(text=tweet_text)
    print(f"ツイートを投稿しました: {tweet_text}")
    print(f"ツイートID: {response.data['id']}")
except Exception as e:
    print(f"ツイート投稿エラー: {str(e)}")
