import openai
import pdfplumber
import PyPDF2 as pypdf
import time
import os
import csv

def get_paper_content(filename=None,use_pypdf=True):
    """ Create pdf object from file

    Parameters
    ----------
    filename : string, optional
        filename for pdf, by default None
    use_pypdf : bool, optional
        choose which pdf library to use, by default True

    Returns
    -------
    list
        list of page objects, one per page in pdf

    """    
    if filename and not use_pypdf:
        return pdfplumber.open(filename).pages
    elif filename and use_pypdf:
        pdfFileObj = open(filename, 'rb')
        pdfReader = pypdf.PdfReader(pdfFileObj)
        return pdfReader.pages
        
def summarize_pages(pages, stop_tag='###---###', type='college student', max_tokens=150):
    """Summarizes pdf pages using openai

    Parameters
    ----------
    pages : list of page objects
        pages of a pdf
    stop_tag : string, optional
        stop string for model, by default '###---###'
    type : str, optional
        reading level of summary output, by default 'college professor'
    max_tokens : int, optional
        maximum number of words in summary, by default 100

    Returns
    -------
    tuple (string, boolean)
        Summary text from model and a boolean flag indicating if the "References" section was encountered
    """    
    
    text = ""
    references_found = False
    
    # Combine texts of all pages in the chunk
    for page in pages:
        page_text = page.extract_text()
        # Check if we've hit the 'References' section
        if "References\n" in page_text:
            # Only keep the part of the text before 'References'
            page_text = page_text.split("References\n")[0]
            text += page_text
            references_found = True
            break
        text += page_text
    
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that summarizes parts of scientific papers for a {type}."},
        {"role": "user", "content": text}
    ]

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                max_tokens=max_tokens
            )
            break
        except openai.error.ServiceUnavailableError:
            print("OpenAI service is unavailable. Retrying in 5 seconds...")
            time.sleep(5)

    return response['choices'][0]['message']['content'], references_found

def generate_summary(api_key, filename):
    openai.api_key = api_key

    paper_content = get_paper_content(filename=filename)
    all_summaries = ""  # Initialize an empty string
    i = 0
    while i < len(paper_content):
        chunk = paper_content[i:i+3]  # Process in chunks of 3 pages
        summary, references_found = summarize_pages(chunk)
        all_summaries = all_summaries +"\n"+ summary  # Append each summary
        # Check if we've hit the 'References' section
        if references_found:
            break
        i += 3
    return all_summaries  # Return the concatenated summaries

def summarize_and_suggest(pre_summary, title):
    """Summarizes pdf pages using openai

    Parameters
    ----------
    pages : list of page objects
        pages of a pdf
    stop_tag : string, optional
        stop string for model, by default '###---###'
    type : str, optional
        reading level of summary output, by default 'college professor'
    max_tokens : int, optional
        maximum number of words in summary, by default 100

    Returns
    -------
    tuple (string, boolean)
        Summary text from model and a boolean flag indicating if the "References" section was encountered
    """    
    
    text = pre_summary
    
    messages = [
        {"role": "system", "content": f"Given the following article from arxiv.org titled ' {title} ', summarize three key insights in a manner understandable to a high school student. For each insight, begin with a relevant emoji that encapsulates the essence of the insight."},
        {"role": "user", "content": text}
    ]

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            break
        except openai.error.ServiceUnavailableError:
            print("OpenAI service is unavailable. Retrying in 5 seconds...")
            time.sleep(5)

    return response['choices'][0]['message']['content']

def translate_into_Russian(text):
    """Summarizes pdf pages using openai

    Parameters
    ----------
    pages : list of page objects
        pages of a pdf
    stop_tag : string, optional
        stop string for model, by default '###---###'
    type : str, optional
        reading level of summary output, by default 'college professor'
    max_tokens : int, optional
        maximum number of words in summary, by default 100

    Returns
    -------
    tuple (string, boolean)
        Summary text from model and a boolean flag indicating if the "References" section was encountered
    """    
    
    messages = [
        {"role": "system", "content": f"You are a helpfull translator. You translate user's messages into Russian."},
        {"role": "user", "content": text}
    ]

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            break
        except openai.error.ServiceUnavailableError:
            print("OpenAI service is unavailable. Retrying in 5 seconds...")
            time.sleep(5)

    return response['choices'][0]['message']['content']

def suggest_intro(text):
    """Summarizes pdf pages using openai

    Parameters
    ----------
    pages : list of page objects
        pages of a pdf
    stop_tag : string, optional
        stop string for model, by default '###---###'
    type : str, optional
        reading level of summary output, by default 'college professor'
    max_tokens : int, optional
        maximum number of words in summary, by default 100

    Returns
    -------
    tuple (string, boolean)
        Summary text from model and a boolean flag indicating if the "References" section was encountered
    """    
    
    messages = [
        {"role": "system", "content": f"You are a famous Russian public speaker and blogger. You can suggest a brilliant intro phrase to start any blog post. User will provide you with the main text of his post, and you will answer with a brief, friendly and informal intro in Russian to kick-off the post. Not more than 5-10 words in Russian - remember to be brief, it's very important! Examples: ""Приветики, народ! Сегодня у нас статья о мультиагентных больших языковых моделях, лец го!"", ""Здорово-здорово! Сейчас поговорим про уязвимости больших языковых моделей."""},
        {"role": "user", "content": text}
    ]

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages
            )
            break
        except openai.error.ServiceUnavailableError:
            print("OpenAI service is unavailable. Retrying in 5 seconds...")
            time.sleep(5)

    return response['choices'][0]['message']['content']

def update_articles_with_blog_posts(openai_api_key, dbFilepath):
    # Open the CSV file for reading
    with open(dbFilepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Read all articles into a list
        articles = list(reader)

    outro_phrase = "@robodream — 3 ключевых инсайта по свежим научным статьям от chatGPT два раза в день"

    # Update the 'blog_post' field for each article
    for article in articles:
        if article['blog_post'] == "":
            title = article['title']
            filename = article['filepath']
            pre_summary = generate_summary(openai_api_key, filename)
            bot_message_en = summarize_and_suggest(pre_summary, title)
            intro_phrase = suggest_intro(bot_message_en)
            bot_message_ru = translate_into_Russian(bot_message_en)
            article['blog_post'] = intro_phrase+'\n'+article['link']+'\n'+'\n'+bot_message_ru+'\n'+"___"+'\n'+outro_phrase

    # Define the field names for the CSV
    fieldnames = ['id', 'link', 'title', 'pdf', 'filepath', 'blog_post', 'posted']

    # Open the CSV file for writing
    with open(dbFilepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the updated articles
        writer.writerows(articles)



def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    db_path = os.getenv("DB_PATH")
    dbFilepath = db_path+'db.csv'
    print("Processing texts with AI...")
    update_articles_with_blog_posts(openai_api_key, dbFilepath)
    print("AI works finished!")

if __name__ == "__main__":
    main()
