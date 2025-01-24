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
    print("以下の環境変数が必要です:")
    print("- TWITTER_API_KEY")
    print("- TWITTER_API_SECRET")
    print("- TWITTER_ACCESS_TOKEN")
    print("- TWITTER_ACCESS_TOKEN_SECRET")
    exit(1)

# Twitter APIの認証
try:
    auth = tweepy.OAuth1UserHandler(
        api_key,
        api_secret,
        access_token,
        access_token_secret
    )
    api = tweepy.API(auth)
    print("Twitter API認証成功!")
except Exception as e:
    print(f"Twitter API認証エラー: {str(e)}")
    exit(1)

# テストツイートを投稿
try:
    tweet_text = "これはテストツイートです。APIが正しく動作しているかを確認しています。"
    api.update_status(tweet_text)
    print(f"ツイートを投稿しました: {tweet_text}")
except Exception as e:
    print(f"ツイート投稿エラー: {str(e)}")
