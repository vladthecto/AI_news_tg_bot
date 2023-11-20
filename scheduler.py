import schedule
import time
import subprocess
import traceback
import os
import http.server
import socketserver
import threading

from http import HTTPStatus

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

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    with socketserver.TCPServer(("", 8080), HealthCheckHandler) as httpd:
        print("serving at port", 8080)
        httpd.serve_forever()

schedule.every().day.at("13:30").do(fetch_articles)
schedule.every().day.at("13:35").do(form_ai_posts)
schedule.every().day.at("15:50").do(telegram_bot)
schedule.every().day.at("10:58").do(telegram_bot)
schedule.every().day.at("09:15").do(cleanup_db)

print('Jobs planned!')

# Run the HTTP server in a separate thread
http_thread = threading.Thread(target=run_http_server)
http_thread.daemon = True  # This ensures the thread will be killed when the main program exits
http_thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
