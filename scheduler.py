import schedule
import time
import subprocess
import traceback
import os

def run_script(script):
    try:
        # get the current environment variables
        env_vars = os.environ.copy()
        # run the script with the current environment variables
        subprocess.run(['/usr/local/bin/python3', script], check=True, env=env_vars)

    except Exception as e:
        print(f"Error occurred while running {script}: {str(e)}")
        print(traceback.format_exc())

def fetch_articles():
    run_script('fetch_articles.py')

def form_ai_posts():
    run_script('form_ai_posts.py')

def telegram_bot():
    run_script('telegram_bot.py')

schedule.every().day.at("17:00").do(fetch_articles)
schedule.every().day.at("11:30").do(form_ai_posts)
schedule.every().day.at("14:56").do(telegram_bot)
schedule.every().day.at("19:10").do(telegram_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
