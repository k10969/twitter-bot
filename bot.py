import os
import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # 追加
from webdriver_manager.chrome import ChromeDriverManager  # 追加

# 設定（変更なし）
TARGET_USERNAME = "_09x"
TWITTER_LOGIN_URL = "https://twitter.com/login"
TWITTER_USER_URL = f"https://twitter.com/{TARGET_USERNAME}"
REPLIES = [
    "今日も元気ですね！",
    "面白いツイートありがとう！",
    "参考になります！"
]
CHECK_INTERVAL = 900
MAX_DAILY_REPLIES = 5

# 環境変数取得（変更なし）
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

class TwitterBot:
    def __init__(self):
        # Chromeオプション設定
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # ChromeDriver自動管理（修正箇所）
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        self.reply_count = 0
        self.last_tweet = None

    # 以下同じ...
        def login(self):
        self.driver.get(TWITTER_LOGIN_URL)
        time.sleep(random.uniform(3, 5))
        self.driver.find_element(By.NAME, "text").send_keys(TWITTER_USERNAME)
        time.sleep(random.uniform(1, 2))
        self.driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'次へ')]").click()
        time.sleep(random.uniform(2, 3))
        self.driver.find_element(By.NAME, "password").send_keys(TWITTER_PASSWORD)
        time.sleep(random.uniform(1, 2))
        self.driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'ログイン')]").click()
        time.sleep(random.uniform(5, 7))

    def get_latest_tweet(self):
        self.driver.get(TWITTER_USER_URL)
        time.sleep(random.uniform(5, 7))
        tweets = self.driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        if tweets:
            return tweets[0].text
        return None

    def send_reply(self, tweet_url):
        if self.reply_count >= MAX_DAILY_REPLIES:
            print("1日のリプライ上限に達しました")
            return

        self.driver.get(tweet_url)
        time.sleep(random.uniform(3, 5))
        self.driver.find_element(By.XPATH, "//div[@aria-label='返信']").click()
        time.sleep(random.uniform(1, 2))
        reply_box = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
        reply_box.send_keys(random.choice(REPLIES))
        time.sleep(random.uniform(1, 2))
        self.driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']").click()
        time.sleep(random.uniform(3, 5))
        self.reply_count += 1
        print(f"リプライ送信: {self.reply_count}/{MAX_DAILY_REPLIES}")

    def run(self):
        self.login()
        while True:
            try:
                current_time = datetime.now()
                if current_time.hour < 7 or current_time.hour > 22:  # 夜間は停止
                    print("夜間は停止中...")
                    time.sleep(3600)
                    continue

                current_tweet = self.get_latest_tweet()
                if current_tweet and current_tweet != self.last_tweet:
                    print("新しいツイートを検出:", current_tweet)
                    tweet_url = self.driver.current_url
                    self.send_reply(tweet_url)
                    self.last_tweet = current_tweet

                sleep_time = CHECK_INTERVAL + random.uniform(-60, 60)  # ランダムな待機時間
                print(f"次のチェックまで{sleep_time}秒待機...")
                time.sleep(sleep_time)

            except Exception as e:
                print(f"エラーが発生しました: {e}")
                time.sleep(600)  # エラー時は10分待機

if __name__ == "__main__":
    bot = TwitterBot()
    bot.run()
