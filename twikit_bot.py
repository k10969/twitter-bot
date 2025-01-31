import twikit
import asyncio
import os
import random
import logging

# Twitterアカウントの監視とリプライを行うボット
class TwitterBot:
    def __init__(self, reply_texts, monitor_accounts):
        self.username = os.getenv('TWITTER_USERNAME')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.reply_texts = reply_texts
        self.monitor_accounts = monitor_accounts
        self.twikit_clients = {}
        self.replies_sent_today = 0
        self.cookie_path = os.path.expanduser("~/.config/twikit/")

        # 初期化の際に各アカウントに対してクライアントを準備
        for i in range(1, 11):
            username = os.getenv(f'TWITTER_USERNAME_{i}')
            password = os.getenv(f'TWITTER_PASSWORD_{i}')
            if username and password:
                self.twikit_clients[username] = {
                    'username': username,
                    'password': password,
                    'client': twikit.Client('ja'),
                    'replies_sent_today': 0
                }

    async def login_to_account(self, client_info):
        try:
            username = client_info['username']
            password = client_info['password']
            client = client_info['client']
            cookies_file = os.path.join(self.cookie_path, f'{username}_cookies.json')

            if os.path.exists(cookies_file):
                client.load_cookies(cookies_file)
            else:
                await client.login(auth_info_1=username, password=password)
                client.save_cookies(cookies_file)
            return client
        except Exception as e:
            logging.error(f"Login failed for {username}: {e}")
            return None

    async def monitor_and_reply(self):
        for username, client_info in self.twikit_clients.items():
            client = await self.login_to_account(client_info)
            if not client:
                continue

            try:
                # 初回実行時に最新ツイートIDを取得
                user = await client.get_user_by_screen_name(username)
                tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
                last_tweet_id = tweets[0].id if tweets else None

                while True:
                    if client_info['replies_sent_today'] < 40:
                        print(f"Checking for new tweets from {username}...")  # Debug log
                        tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
                        latest_tweet = tweets[0] if tweets else None
                        if latest_tweet:
                            print(f"Latest tweet ID: {latest_tweet.id}")  # Debug log
                        if latest_tweet and latest_tweet.id != last_tweet_id:
                            reply_text = random.choice(self.reply_texts)
                            if latest_tweet.text == reply_text:  # 投稿が被る場合
                                reply_text += " - New Reply!"
                            print(f"Replying to tweet ID: {latest_tweet.id} with: {reply_text}")  # Debug log
                            await client.create_tweet(text=reply_text, reply_to=latest_tweet.id)
                            client_info['replies_sent_today'] += 1
                            last_tweet_id = latest_tweet.id
                            print(f"Replied to tweet {latest_tweet.id}")
                        else:
                            print("No new tweets to reply to.")  # Debug log
                    else:
                        print(f"Daily reply limit reached for {username}.")
                    await asyncio.sleep(300)  # 5分ごとにチェック
            except Exception as e:
                logging.error(f"Error occurred for {username}: {e}")
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

    # 環境変数で管理するアカウントをリスト化
    monitor_accounts = [os.getenv(f'MONITOR_ACCOUNT_{i}') for i in range(1, 11) if os.getenv(f'MONITOR_ACCOUNT_{i}')]

    # ボットの初期化
    bot = TwitterBot(reply_texts=reply_texts, monitor_accounts=monitor_accounts)

    # ボットの実行
    asyncio.run(bot.monitor_and_reply())
