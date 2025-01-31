import twikit
import asyncio
import os
import random
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

# Twitterアカウントの監視とリプライを行うボット
class TwitterBot:
    def __init__(self, reply_texts, monitor_accounts):
        self.username = os.getenv('TWITTER_USERNAME')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.reply_texts = reply_texts
        self.monitor_accounts = monitor_accounts
        self.twikit_clients = {}
        self.replies_sent_today = {account: 0 for account in monitor_accounts}
        self.cookie_path = os.path.expanduser("~/.config/twikit/")

        # アカウントごとにクライアントを準備
        for account in monitor_accounts:
            self.twikit_clients[account] = {
                'client': twikit.Client('ja'),
                'last_tweet_id': None
            }

    async def login_to_account(self, account, client_info):
        try:
            client = client_info['client']
            cookies_file = os.path.join(self.cookie_path, f'{account}_cookies.json')

            # クッキーがあれば読み込み、なければログインして保存
            if os.path.exists(cookies_file):
                client.load_cookies(cookies_file)
            else:
                await client.login(auth_info_1=self.username, auth_info_2=self.username, password=self.password)
                client.save_cookies(cookies_file)

            logging.info(f"Logged in successfully for {account}.")
            return client
        except Exception as e:
            logging.error(f"Login failed for {account}: {e}")
            return None

    async def monitor_and_reply(self):
        for account, client_info in self.twikit_clients.items():
            client = await self.login_to_account(account, client_info)
            if not client:
                continue

            try:
                # 初回実行時に最新ツイートIDを取得
                user = await client.get_user_by_screen_name(account)
                tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
                last_tweet_id = tweets[0].id if tweets else None
                self.twikit_clients[account]['last_tweet_id'] = last_tweet_id

                while True:
                    if self.replies_sent_today[account] < 40:
                        logging.info(f"Checking for new tweets from {account}...")  # Debug log
                        tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
                        latest_tweet = tweets[0] if tweets else None

                        if latest_tweet:
                            logging.info(f"Latest tweet ID: {latest_tweet.id}")  # Debug log
                        if latest_tweet and latest_tweet.id != last_tweet_id:
                            reply_text = random.choice(self.reply_texts)
                            logging.info(f"Replying to tweet ID: {latest_tweet.id} with: {reply_text}")  # Debug log
                            await client.create_tweet(text=reply_text, reply_to=latest_tweet.id)
                            self.replies_sent_today[account] += 1
                            last_tweet_id = latest_tweet.id
                            logging.info(f"Replied to tweet {latest_tweet.id}")
                        else:
                            logging.info(f"No new tweets to reply to from {account}.")  # Debug log
                    else:
                        logging.info(f"Daily reply limit reached for {account}.")
                    await asyncio.sleep(300)  # 5分ごとにチェック
            except Exception as e:
                logging.error(f"Error occurred for {account}: {e}")
                await asyncio.sleep(600)  # エラー発生時は10分待機

        # 全てのアカウントからログアウト
        for client_info in self.twikit_clients.values():
            await client_info['client'].logout()

# 使用例
if __name__ == "__main__":
    # リプライメッセージのリスト
    reply_texts = [
        "Thank you for your tweet!",
        "We appreciate your feedback!",
        "Stay tuned for more updates!"
    ]

    # 環境変数から監視するアカウントを取得（カンマ区切りで複数指定）
    monitor_accounts = os.getenv('MONITOR_ACCOUNT', '').split(',')

    # ボットの初期化
    bot = TwitterBot(reply_texts=reply_texts, monitor_accounts=monitor_accounts)

    # ボットの実行
    asyncio.run(bot.monitor_and_reply())
