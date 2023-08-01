import os
import csv

def cleanup_db(dbFilepath):
    # Open the CSV file for reading
    with open(dbFilepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Read all articles into a list
        articles = list(reader)

    # Iterate over the articles
    for article in articles:
        # Check if the article has been posted
        if article['posted'] == "True":
            # Get the file path
            filepath = article['filepath']
            
            # Check if the file exists
            if os.path.exists(filepath):
                try:
                    # Delete the file
                    os.remove(filepath)
                    print(f"Deleted file: {filepath}")
                except Exception as e:
                    print(f"Error while deleting file {filepath}: {e}")

if __name__ == "__main__":
    db_path = os.getenv("DB_PATH")
    dbFilepath = db_path+'db.csv'
    cleanup_db(dbFilepath)
