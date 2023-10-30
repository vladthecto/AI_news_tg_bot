import os
import csv

def cleanup_db_rows(filename='./db.csv'):
    # Read all rows from the CSV
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Filter rows based on the given conditions
    filtered_rows = [row for row in rows if not (row['posted'] == "False" and "@robodream — chatGPT читает научные статьи и подсвечивает инсайты" not in row['blog_post'])]

    # Write the filtered rows back to the CSV
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Cleanup completed for {filename}!")

if __name__ == "__main__":
    db_path = os.getenv("DB_PATH")
    dbFilepath = db_path+'db.csv'
    cleanup_db_rows(dbFilepath)
