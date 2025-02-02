import twikit
import asyncio
import os
import random

# Twitterアカウントの監視とリプライを行うボット
class TwitterBot:
    def __init__(self, reply_texts, monitor_account):
        self.username = os.getenv('TWITTER_USERNAME')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.reply_texts = reply_texts
        self.monitor_account = monitor_account
        self.twikit_client = twikit.Client('ja')
        self.replies_sent_today = 0
        self.cookie_path = os.path.expanduser("~/.config/twikit/twikit_cookies.json")

    async def monitor_and_reply(self):
        last_tweet_id = None
        cookie_dir = os.path.dirname(self.cookie_path)
        if not os.path.exists(cookie_dir):
            os.makedirs(cookie_dir)
        if os.path.exists(self.cookie_path):
            self.twikit_client.load_cookies(self.cookie_path)
        else:
            try:
                await self.twikit_client.login(auth_info_1=self.username, auth_info_2=self.username, password=self.password)
                self.twikit_client.save_cookies(self.cookie_path)
            except twikit.errors.TwitterException as e:
                print(f"Login error: {e}")
                return

        # 初回実行時に最新ツイートIDを取得
        user = await self.twikit_client.get_user_by_screen_name(self.monitor_account)
        tweets = await self.twikit_client.get_user_tweets(user.id, 'Tweets', count=1)
        if tweets:
            last_tweet_id = tweets[0].id

        while True:
            try:
                if self.replies_sent_today < 40:
                    print("Checking for new tweets...")  # Debug log
                    tweets = await self.twikit_client.get_user_tweets(user.id, 'Tweets', count=1)
                    latest_tweet = tweets[0] if tweets else None
                    if latest_tweet:
                        print(f"Latest tweet ID: {latest_tweet.id}")  # Debug log
                    if latest_tweet and latest_tweet.id != last_tweet_id:
                        reply_text = random.choice(self.reply_texts)
                        print(f"Replying to tweet ID: {latest_tweet.id} with: {reply_text}")  # Debug log
                        await self.twikit_client.create_tweet(text=reply_text, reply_to=latest_tweet.id)
                        self.replies_sent_today += 1
                        last_tweet_id = latest_tweet.id
                        print(f"Replied to tweet {latest_tweet.id}")
                    else:
                        print("No new tweets to reply to.")  # Debug log
                else:
                    print("Daily reply limit reached.")
                await asyncio.sleep(300)  # 5分ごとにチェック
            except Exception as e:
                print(f"Error occurred: {e}")
                await asyncio.sleep(600)  # エラー発生時は10分待機

        await self.twikit_client.logout()

# 使用例
if __name__ == "__main__":
    # リプライメッセージのリスト
    reply_texts = [
        "Thank you for your tweet!",
        "We appreciate your feedback!",
        "Stay tuned for more updates!"
    ]

    # 監視するアカウント
    monitor_account = os.getenv('MONITOR_ACCOUNT')

    # ボットの初期化
    bot = TwitterBot(reply_texts=reply_texts, monitor_account=monitor_account)

    # ボットの実行
    asyncio.run(bot.monitor_and_reply())
