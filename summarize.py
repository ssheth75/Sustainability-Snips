import requests
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from newspaper import Article
from datetime import date
from keys import API_KEY

# Make a request to the Google Search API

# Make News API request
currentDate = date.today().isoformat()

url = ('https://newsapi.org/v2/everything?'
       'q=sustainability&'
       f'from=(currentDate)&'
       'sortBy=popularity&'
       f'apiKey={API_KEY}')

response = requests.get(url)

print(response.json())


# Extracting the links from the response object
data = response.json()
links = []

if 'articles' in data:
    articles = data['articles']
    count = 0
    for article in articles:
        if 'url' in article:
            links.append(article['url'])
            count += 1
            if count == 15:  # Stop after the first 15 articles
                break

print(links)

# Store data in dataframe

df = pd.DataFrame(columns=['Title', 'URL', 'Authors', 'Date', 'Summary', 'Image'])
nltk.download('punkt')

for url in links:
    article = Article(url)
    article.download()
    article.parse()
    
    article.nlp()

    if article.title == '':
        article.title = 'No title listed'

    if article.authors == []:
        article.authors = ['No author listed']
    else:
        article.authors = ", ".join(article.authors)

    if article.publish_date == None:
        article.publish_date = 'No date listed'

    if article.summary == '':
        article.summary = 'No summary listed'   
    
    if article.top_image == '':
        article.top_image = 'No image listed'

    dfInstance = {
        'Title': article.title,
        'URL': url,
        'Authors': article.authors,
        'Date': article.publish_date,
        'Summary': article.summary,
        'Image': article.top_image
    }

    df = pd.concat([df, pd.DataFrame(dfInstance, index=[0])], ignore_index=True)

print(df)

        

# print(url)
