import requests
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from newspaper import Article
from datetime import date, timedelta
from keys import API_KEY

# Make a request to the Google Search API

# Make News API request
currentDate = date.today().isoformat()


url = ('https://newsapi.org/v2/everything?'
       'q=climate change&'
       'from=2023-07-05&'
       'sortBy=relavance&'
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

# Store data in DataFrame
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

    if article.publish_date is None:
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

# Load HTML template
with open('template.html', 'r') as file:
    template = file.read()

# Generate HTML content
html_content = ""
for i, row in df.iterrows():
    card_html = """
    <div class="card_item">
        <div class="card_inner">
            <img src="{image}">
            <div class="title">{title}</div>
            <div class="author">{authors}</div>
            <div class="summary">{summary}</div>
        </div>
    </div>
    """.format(image=row['Image'], title=row['Title'], authors=row['Authors'], summary=row['Summary'])
    html_content += card_html

# Replace the placeholder in the template with the generated HTML content
new_html = template.replace('{{content}}', html_content)

# Save the modified template with the DataFrame data to a new HTML file
with open('index.html', 'w') as file:
    file.write(new_html)
