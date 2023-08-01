import csv
import os
import requests
import feedparser
from datetime import datetime, timedelta
import shutil

def fetch_arxiv_articles(query, max_results=1000):
    base_url = 'http://export.arxiv.org/api/query?'
    
    # date 3 days ago from now
    time_delta = datetime.now() - timedelta(days=3)

    # build the query parameters
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(base_url, params=params)
    feed = feedparser.parse(response.content)

    # filter the articles from the last 3 days
    recent_articles = [entry for entry in feed.entries if datetime(*entry.published_parsed[:6]) >= time_delta]

    return recent_articles

def save_articles_to_csv(articles, filename):
    # define the CSV columns
    fieldnames = ["id", "link", "title", "pdf", "filepath", "blog_post", "posted"]

    # read the existing data
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = [row for row in reader]
    except FileNotFoundError:
        existing_data = []

    # collect the existing IDs
    existing_ids = {row['id'] for row in existing_data}

    # write to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write the header row
        writer.writeheader()

        # write the existing data
        writer.writerows(existing_data)

        for article in articles:
            # extract the ID
            id = article.id.split('/')[-1]

            # check if the article is already in the CSV
            if id not in existing_ids:
                # extract the PDF link
                pdf_link = article.link.replace('abs', 'pdf') + ".pdf"

                # write the article data to the CSV file
                writer.writerow({
                    "id": id,
                    "link": article.link,
                    "title": article.title,
                    "pdf": pdf_link,
                    "filepath": "",
                    "blog_post": "",
                    "posted": False
                })

def download_pdfs(db_path, dbFilepath):
    articles = []
    
    # read the CSV file
    with open(dbFilepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # iterate over the articles
        for article in reader:
            if article['filepath'] == "":
                # get the ID and PDF link
                id = article['id']
                pdf_link = article['pdf']
                
                # make a GET request to download the PDF
                response = requests.get(pdf_link)
                
                # ensure the DB directory exists
                os.makedirs(db_path, exist_ok=True)

                pdfFilepath = db_path + f'{id}.pdf'
                
                # write the content to a PDF file
                with open(pdfFilepath, 'wb') as f:
                    f.write(response.content)
                
                article['filepath'] = pdfFilepath
            
            articles.append(article)
    
    # write the articles to a new CSV file
    with open('new.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'link', 'title', 'pdf', 'filepath', 'blog_post', 'posted']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    
    # replace the old CSV file with the new one
    shutil.move('new.csv', dbFilepath)

def checkfile(filename):
# open the csv file
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # iterate over the articles
        for article in reader:
            print(article) 


def main():
    # use this function to fetch the articles
    db_path = os.getenv("DB_PATH")
    dbFilepath = db_path+'db.csv'
    articles = fetch_arxiv_articles("all:AI OR all:AGI OR all:LLM", 5)
    # save the articles to a CSV file
    print("Fetching fresh articles...")
    save_articles_to_csv(articles, dbFilepath)
    print("Saved to csv...")
    print("Downloading PDFs...")
    download_pdfs(db_path, dbFilepath)
    print("All done!")
    

if __name__ == "__main__":
    main()