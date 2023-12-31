import os
import csv
import asyncio
from aiogram import Bot, Dispatcher, types

def compose_message(data):
    return data['blog_post']

async def send_messages(token, chat_id, db_path):
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    dbFilepath = db_path+'db.csv'

    # Define the field names for the CSV
    fieldnames = ['id', 'link', 'title', 'pdf', 'filepath', 'blog_post', 'posted']

    # Open the CSV file for reading
    with open(dbFilepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Read all articles into a list
        articles = list(reader)
        articles.reverse()

    # Iterate over the articles
    for article in articles:
        if article['blog_post'] != "" and article['posted'] == "False":
            
            message = compose_message(article)
            
            # Send the blog post
            await bot.send_message(chat_id, message)
            
            # Mark the article as posted
            article['posted'] = "True"
            break
            
    # Open the CSV file for writing
    with open(dbFilepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        articles.reverse()
        
        # Write the updated articles
        writer.writerows(articles)

    await bot.close()

def main():
    tg_bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    db_path = os.getenv("DB_PATH")
    print('Sending messages...')
    asyncio.run(send_messages(tg_bot_token, chat_id, db_path))
    print('Message sent!')

if __name__ == "__main__":
    main()

