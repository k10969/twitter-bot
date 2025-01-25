import os
import asyncio
import random
from datetime import datetime
from twikit import Client
from twikit.errors import TwitterError

# 環境変数設定
TWITTER_USER = os.getenv('TWITTER_USERNAME')
TWITTER_PASS = os.getenv('TWITTER_PASSWORD')
TARGET_USER = os.getenv('TARGET_ACCOUNT')
MAX_REPLIES = 40

class TwitterBot:
    def __init__(self):
        self.client = Client('ja-JP')
        self.reply_count = 0
        self.last_reset = datetime.now()

    async def initialize(self):
        try:
            if os.path.exists('auth.json'):
                self.client.load_auth('auth.json')
            else:
                await self.client.login(
                    account=TWITTER_USER,
                    password=TWITTER_PASS
                )
                self.client.save_auth('auth.json')
        except TwitterError as e:
            print(f"認証エラー: {e}")
            exit(1)

    async def run(self):
        await self.initialize()
        while True:
            try:
                if (datetime.now() - self.last_reset).days >= 1:
                    self.reply_count = 0
                    self.last_reset = datetime.now()
                
                user = await self.client.get_user(TARGET_USER)
                tweets = await user.get_tweets('Tweets')
                
                for tweet in reversed(tweets):
                    if self.reply_count < MAX_REPLIES:
                        await tweet.reply(random.choice([
                            "参考になります！",
                            "素晴らしい情報をありがとうございます"
                        ]))
                        self.reply_count += 1
                        await asyncio.sleep(random.randint(120, 600))
            except TwitterError as e:
                print(f"エラー発生: {e}")
                await asyncio.sleep(3600)  # 1時間待機

if __name__ == "__main__":
    bot = TwitterBot()
    asyncio.run(bot.run())
