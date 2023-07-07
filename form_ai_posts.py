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

def summarize_and_suggest(pre_summary):
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
        {"role": "system", "content": "You are a helpfull assitant, Ted talks speaker, Harvard graduate and an incredibly experienced entrepreneur'\
         in the technology sector who is known for being great at seeing scientific advances as opportunities to solve society's problems.'\
         User will provide you with the summary of recently published research paper (it was done by AI, processing chunks of 3 pages each, '\
         so ignore some possible inconsistency in the text). Please form your answer following this 4-parts logic: '\
         1.Suggest an emoji which's the most appropriate for this paper based on your sentiment after reading, use this emoji as the first symbol of your answer. '\
         2.Assess the potential for the inferences described in the article to already be put into practice in the next few months. '\
         Give a score from 1 to 5, where 1 can be used in further research, but is not applicable in practice yet, and 5 can be used in '\
         applied solutions in a couple of months if there is an interested team. Formulate this part as "" My grade: <x> Elons out of 5."" and nothing else. '\
         3.Add your brief retelling of this research paper and its conclusions - just 5 brief sentences, not more. Start this part with ""Summary:"" '\
         4.Offer one imaginary future product based on the science from this paper and describe it just in 4-5 brief sentences, include a specific example of '\
         its implementation in real life. Start this part with ""My vision:"". '\
         Please try to use friendly, explanative and motivating tone of voice, pretend you're Elon Musk and you're explaining this paper results '\
         to high school students and motivating them to start up a project in this field."},
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
        {"role": "system", "content": f"You are a famous Russian public speaker and blogger. You can suggest a brilliant intro phrase to start any blog post. User will provide you with the main text of his post, and you will answer with a brief, friendly and informal intro to kick-off the post (up to 10 words). Examples: ""Здорово, народ! Сегодня у нас статья об искусственном интеллекте!"" "},
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

def update_articles_with_blog_posts(openai_api_key):
    # Open the CSV file for reading
    with open('./db.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Read all articles into a list
        articles = list(reader)

    # Update the 'blog_post' field for each article
    for article in articles:
        if article['blog_post'] == "":
            filename = article['filepath']
            pre_summary = generate_summary(openai_api_key, filename)
            bot_message_en = summarize_and_suggest(pre_summary)
            bot_message_ru = translate_into_Russian(bot_message_en)
            article['blog_post'] = bot_message_ru

    # Define the field names for the CSV
    fieldnames = ['id', 'link', 'title', 'pdf', 'filepath', 'blog_post', 'posted']

    # Open the CSV file for writing
    with open('./db.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the updated articles
        writer.writerows(articles)



def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    print("Processing texts with AI...")
    update_articles_with_blog_posts(openai_api_key)
    print("AI works finished!")

if __name__ == "__main__":
    main()
