import os
import asyncio
import random
from datetime import datetime
from twikit import Client, TwitterError

# 環境変数設定
TWITTER_USER = os.getenv('TWITTER_USERNAME')
TWITTER_PASS = os.getenv('TWITTER_PASSWORD')
TARGET_USER = os.getenv('TARGET_ACCOUNT')  # @なしのスクリーンネーム
MAX_REPLIES = 40

class AdvancedTwitterBot:
    def __init__(self):
        self.client = Client('ja-JP')
        self.reply_counter = 0
        self.last_reset = datetime.now()
        self.processed = set()

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
            print(f"認証失敗: {e}")
            exit(1)

    async def monitor_account(self):
        try:
            user = await self.client.get_user(TARGET_USER)
            tweets = await user.get_tweets('Tweets')
            
            for tweet in reversed(tweets):
                if tweet.id not in self.processed:
                    if self.check_limits():
                        await self.smart_reply(tweet)
                        self.processed.add(tweet.id)
                        self.reply_counter += 1
                    else:
                        print("⚠️ 本日の上限到達")
                        return
        except TwitterError as e:
            print(f"監視エラー: {e}")

    async def smart_reply(self, tweet):
        try:
            replies = [
                "参考になります！",
                "素晴らしい情報を共有いただき感謝します",
                "勉強になります！"
            ]
            await tweet.reply(random.choice(replies))
            print(f"✅ リプライ成功: {tweet.id}")
            await asyncio.sleep(random.randint(120, 600))  # 安全待機時間
        except TwitterError as e:
            print(f"リプライ失敗: {e}")

    def check_limits(self):
        # 日次リセット & レート制限チェック
        if (datetime.now() - self.last_reset).days >= 1:
            self.reply_counter = 0
            self.last_reset = datetime.now()
        return self.reply_counter < MAX_REPLIES

    async def run(self):
        await self.initialize()
        while True:
            await self.monitor_account()
            await asyncio.sleep(random.randint(1800, 3600))  # 30-60分間隔

if __name__ == "__main__":
    bot = AdvancedTwitterBot()
    asyncio.run(bot.run())
