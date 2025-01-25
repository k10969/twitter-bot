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
