import os
import asyncio
import random
from datetime import datetime
from twikit import Client

# 環境変数から設定取得
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
TARGET_ACCOUNT = os.getenv('TARGET_ACCOUNT')  # 追加
MAX_DAILY_REPLIES = 40

# 環境変数チェック
if not all([TWITTER_USERNAME, TWITTER_PASSWORD, TARGET_ACCOUNT]):
    raise ValueError("必要な環境変数が設定されていません")

class TwitterBot:
    def __init__(self):
        self.client = Client('ja-JP')
        self.processed_tweets = set()
        self.reply_count = 0

    async def initialize(self):
        if os.path.exists('cookies.json'):
            self.client.load_cookies('cookies.json')
        else:
            await self.client.login(
                auth_info_1=TWITTER_USERNAME,
                password=TWITTER_PASSWORD
            )
            self.client.save_cookies('cookies.json')

    async def check_tweets(self):
        try:
            user = await self.client.get_user_by_screen_name(TARGET_ACCOUNT)
            tweets = await self.client.get_user_tweets(user.id, 'Tweets')
            
            for tweet in reversed(tweets):
                if tweet.id not in self.processed_tweets:
                    if self.reply_count < MAX_DAILY_REPLIES:
                        await self.reply_to_tweet(tweet)
                        self.processed_tweets.add(tweet.id)
                        self.reply_count += 1
                    else:
                        print("⚠️ 本日のリプライ上限到達")
        except Exception as e:
            print(f"監視エラー: {str(e)}")

    async def reply_to_tweet(self, tweet):
        try:
            replies = ["参考になります！", "素晴らしい情報をありがとう！"]
            await tweet.reply(random.choice(replies))
            print(f"✅ リプライ成功: {tweet.id}")
            await asyncio.sleep(random.randint(60, 300))
        except Exception as e:
            print(f"リプライ失敗: {str(e)}")

    async def run(self):
        await self.initialize()
        while True:
            if datetime.now().hour == 0:  # 日次リセット
                self.reply_count = 0
                self.processed_tweets.clear()
            
            await self.check_tweets()
            await asyncio.sleep(random.randint(900, 2700))

if __name__ == "__main__":
    bot = TwitterBot()
    asyncio.run(bot.run())
