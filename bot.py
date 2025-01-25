import os
import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設定
TARGET_USERNAME = "_09x"
TWITTER_LOGIN_URL = "https://twitter.com/login"
TWITTER_USER_URL = f"https://twitter.com/{TARGET_USERNAME}"
REPLIES = ["今日も元気ですね！", "面白いツイートありがとう！"]
CHECK_INTERVAL = 1800  # 30分間隔
MAX_DAILY_REPLIES = 5

class TwitterBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.reply_count = 0
        self.last_tweet = None

    def login(self):
        self.driver.get(TWITTER_LOGIN_URL)
        time.sleep(random.uniform(3,5))
        # ログイン処理（環境変数を使用）
        username = os.getenv("TWITTER_USERNAME")
        password = os.getenv("TWITTER_PASSWORD")
        self.driver.find_element(By.NAME, "text").send_keys(username)
        self.driver.find_element(By.XPATH, "//div[text()='次へ']").click()
        time.sleep(2)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//div[text()='ログイン']").click()
        time.sleep(5)

    def run(self):
        self.login()
        while True:
            try:
                self.check_tweets()
                time.sleep(CHECK_INTERVAL + random.randint(-300, 300))
            except Exception as e:
                print(f"エラー発生: {str(e)}")
                time.sleep(600)

if __name__ == "__main__":
    bot = TwitterBot()
    bot.run()
