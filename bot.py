import os
import asyncio
import random
from datetime import datetime, timedelta
from twikit import Client

# 環境変数設定
USERNAME = os.getenv('TWITTER_USERNAME')
PASSWORD = os.getenv('TWITTER_PASSWORD')
TARGET_ACCOUNT = '@監視対象アカウント'  # @を含まないスクリーンネーム
MAX_DAILY_REPLIES = 40
REPLIES = ["参考になります！", "素敵な情報をありがとう！"]

class TwitterBot:
    def __init__(self):
        self.client = Client('ja-JP')
        self.processed_tweets = set()
        self.reply_count = 0
        self.last_check = datetime.now() - timedelta(days=1)

    async def initialize(self):
        if os.path.exists('cookies.json'):
            self.client.load_cookies('cookies.json')
        else:
            await self.client.login(
                auth_info_1=USERNAME,
                password=PASSWORD
            )
            self.client.save_cookies('cookies.json')

    async def check_new_tweets(self):
        user = await self.client.get_user_by_screen_name(TARGET_ACCOUNT)
        tweets = await self.client.get_user_tweets(user.id, 'Tweets')
        
        for tweet in reversed(tweets):
            if tweet.id not in self.processed_tweets:
                if self.reply_count < MAX_DAILY_REPLIES:
                    await self.send_reply(tweet)
                    self.processed_tweets.add(tweet.id)
                    self.reply_count += 1
                else:
                    print("本日のリプライ上限に到達")

    async def send_reply(self, tweet):
        try:
            await tweet.reply(random.choice(REPLIES))
            print(f"リプライ送信: {tweet.id}")
            await asyncio.sleep(random.randint(60, 300))  # ランダム待機
        except Exception as e:
            print(f"エラー: {str(e)}")

    async def run(self):
        await self.initialize()
        while True:
            if datetime.now().date() != self.last_check.date():
                self.reply_count = 0
                self.last_check = datetime.now()
            
            await self.check_new_tweets()
            sleep_time = random.randint(900, 2700)  # 15-45分ランダム
            print(f"次のチェックまで{sleep_time}秒待機")
            await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    bot = TwitterBot()
    asyncio.run(bot.run())
