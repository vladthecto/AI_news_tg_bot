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
        subprocess.run(['python', script], check=True, env=env_vars)

    except Exception as e:
        print(f"Error occurred while running {script}: {str(e)}")
        print(traceback.format_exc())

def fetch_articles():
    run_script('fetch_articles.py')

def form_ai_posts():
    run_script('form_ai_posts.py')

def telegram_bot():
    run_script('telegram_bot.py')

def cleanup_db():
    run_script('cleanup_db.py')

schedule.every().day.at("10:30").do(fetch_articles)
schedule.every().day.at("10:40").do(form_ai_posts)
schedule.every().day.at("16:50").do(telegram_bot)
schedule.every().day.at("10:58").do(telegram_bot)
schedule.every().day.at("20:15").do(cleanup_db)
print('Jobs planned!')

while True:
    schedule.run_pending()
    time.sleep(1)
