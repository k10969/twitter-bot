import twikit
import asyncio
import os
import random

class TwitterBot:
    def __init__(self, accounts, monitor_accounts, reply_texts):
        self.accounts = accounts
        self.monitor_accounts = monitor_accounts
        self.reply_texts = reply_texts
        self.extra_words = ["Nice!", "Cool!", "Awesome!", "Great!", "🔥", "😊", "💡"]
        self.clients = {}
        self.replies_sent_today = {account["username"]: 0 for account in self.accounts}
        self.last_reply_texts = {account["username"]: {} for account in self.accounts}
        self.cookie_path_template = os.path.expanduser("~/.config/twikit/{username}_cookies.json")

    async def login_all_accounts(self):
        """ 全アカウントでログイン処理 """
        for account in self.accounts:
            username, password = account["username"], account["password"]
            cookie_path = self.cookie_path_template.format(username=username)
            client = twikit.Client('ja')

            try:
                if os.path.exists(cookie_path):
                    client.load_cookies(cookie_path)
                else:
                    await client.login(auth_info_1=username, auth_info_2=username, password=password)
                    client.save_cookies(cookie_path)

                self.clients[username] = client
                print(f"[INFO] {username} - ログイン成功")

            except Exception as e:
                print(f"[ERROR] {username} - ログイン失敗: {e}")

    async def monitor_and_reply(self, username, client):
        """ 指定アカウントでツイートを監視し、リプライを送信 """
        last_tweet_ids = {account: None for account in self.monitor_accounts}

        while True:
            try:
                if self.replies_sent_today[username] < 30:
                    for account in self.monitor_accounts:
                        user = await client.get_user_by_screen_name(account)
                        tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
                        latest_tweet = tweets[0] if tweets else None

                        if latest_tweet and latest_tweet.id != last_tweet_ids[account]:
                            reply_text = random.choice(self.reply_texts)
                            if reply_text == self.last_reply_texts[username].get(account, ""):
                                reply_text += " " + random.choice(self.extra_words)

                            await client.create_tweet(text=reply_text, reply_to=latest_tweet.id)
                            self.replies_sent_today[username] += 1
                            last_tweet_ids[account] = latest_tweet.id
                            self.last_reply_texts[username][account] = reply_text
                            print(f"[INFO] {username} - {account} にリプライ: {reply_text}")

                            await asyncio.sleep(5)  # APIリクエスト間隔

                else:
                    print(f"[INFO] {username} - 1日のリプライ上限に達しました")

                await asyncio.sleep(random.randint(180, 600))  # 3分〜10分待機

            except Exception as e:
                print(f"[ERROR] {username} - エラー発生: {e}")
                await asyncio.sleep(600)  # 10分待機後に再試行

    async def start_all(self):
        """ すべてのアカウントで監視を開始 """
        await self.login_all_accounts()
        tasks = [self.monitor_and_reply(username, client) for username, client in self.clients.items()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 環境変数からアカウント情報を取得
    accounts = [
        {"username": os.getenv(f"TWITTER_USERNAME_{i}"), "password": os.getenv(f"TWITTER_PASSWORD_{i}")}
        for i in range(1, 11)
        if os.getenv(f"TWITTER_USERNAME_{i}") and os.getenv(f"TWITTER_PASSWORD_{i}")
    ]
    
    # 環境変数から監視するアカウントを取得
    monitor_accounts = [
        os.getenv(f"MONITOR_ACCOUNT_{i}") for i in range(1, 11) if os.getenv(f"MONITOR_ACCOUNT_{i}")
    ]

    # リプライメッセージのリスト
    reply_texts = [
        "Thank you!", "Great post!", "Nice update!", "Awesome work!", "Keep it up!", "🔥🔥🔥"
    ]

    # ボットの実行
    bot = TwitterBot(accounts=accounts, monitor_accounts=monitor_accounts, reply_texts=reply_texts)
    asyncio.run(bot.start_all())
