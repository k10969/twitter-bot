import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 設定
TARGET_USERNAME = "_09x"
CHECK_INTERVAL = 1800  # 30分間隔
MAX_DAILY_REPLIES = 5

class TwitterBot:
    def __init__(self):
        options = Options()
        options.binary_location = "/usr/bin/chromium"  # Render用パス
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        # ChromeDriver自動管理
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options
        )
        self.reply_count = 0

    def login(self):
        self.driver.get("https://twitter.com/login")
        time.sleep(random.uniform(3,5))
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
                # ツイート監視処理
                time.sleep(CHECK_INTERVAL)
            except Exception as e:
                print(f"エラー発生: {str(e)}")
                time.sleep(600)

if __name__ == "__main__":
    bot = TwitterBot()
    bot.run()
