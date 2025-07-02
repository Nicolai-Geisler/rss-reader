import getpass
import os
import feedparser
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Read the .env file
load_dotenv()

# Class for storing articles from rss feed data
class Article:
    def __init__(self, title, link, description, published, img):
        self.title = title
        self.link = link
        self.description = description
        self.published = published
        self.img = img

    def __str__(self):
        return f"{self.title}\n{self.link}\n{self.description}\n{self.published}\n{self.img}"

# Store all articles in Array
articles = []

# Parse the RSS feed
feed_url = "https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml"
feed = feedparser.parse(feed_url)

for entry in feed.entries:

    # Handle different possible locations of the content
    content = None
    img = None
    
    # Case 1: content:encoded field exists directly
    if 'content:encoded' in entry:
        content = entry['content:encoded']
    # Case 2: content field exists as a list of dictionaries
    elif 'content' in entry:
        if isinstance(entry.content, list):
            # Take the first content item's value
            content = entry.content[0].value
        else:
            content = entry.content
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        img_tag = soup.find('img')
        
        if img_tag and img_tag.get('src'):
            img = img_tag['src']
        else:
            img = ""
    else:
        img = ""
        print("No content available in this entry")
    
    article = Article(entry.title, entry.link, entry.published, entry.description, img)
    articles.append(article)

# Basic feed information
print(f"Feed Title: {feed.feed.title}")
print(f"Feed Description: {feed.feed.description}")
print(f"Feed Link: {feed.feed.link}\n")

# Print all articles
for article in articles:
    print(article)
    print("\n")
