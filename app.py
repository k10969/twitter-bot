import os
import asyncio
from flask import Flask
from twikit import Client

app = Flask(__name__)

# 環境変数から認証情報を取得
EMAIL = os.getenv('EMAIL')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
KEYWORD = os.getenv('KEYWORD', '東京都知事')

client = Client('ja')

async def twitter_task():
    if os.path.exists('cookies.json'):
        client.load_cookies('cookies.json')
    else:
        await client.login(
            auth_info_1=EMAIL,
            auth_info_2=USERNAME,
            password=PASSWORD
        )
        client.save_cookies('cookies.json')
    
    tweets = await client.search_tweet(KEYWORD, 'Top', count=5)
    return [tweet.text for tweet in tweets]

@app.route('/')
async def index():
    try:
        tweets = await twitter_task()
        return {
            "status": "success",
            "tweets": tweets
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
