#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests as req

# https://github.com/egorsmkv/rfeed
from feedgen.feed import FeedGenerator


# In[2]:


RUMBLE_URL = "https://rumble.com/c/"
USERNAME = ""

URL = f"{RUMBLE_URL}{USERNAME}"

PAGES = 15


# In[3]:


pages = []

for n in range(0, PAGES):
    if USERNAME == "": # Putting this here to avoid ipython issues
        break
    
    page_raw = req.get(f"{URL}?page={n}")
    
    page_soup = bs(page_raw.content, 'html.parser')
    
    if page_soup.h1.text == "404 - Not found":
        break

    
    pages.append(page_soup.find_all("article"))


# In[4]:


data_dict = []

for article_page in pages:
    for article in article_page:
        data_dict.append({
            'title': article.h3.text,
            'date': article.time["datetime"],
            'duration': article.span["data-value"],
            'URL': article.a["href"]
        })


# In[5]:


feed = FeedGenerator()
feed.id(URL)
feed.title(f" {USERNAME} ")
feed.link(rel="self", href=URL)
feed.description(f" {USERNAME} ") # Requires a description but none given on Rumble

for item in data_dict:
    entry = feed.add_entry()
    entry.id(item['URL'])
    entry.title(item["title"])
    entry.pubDate(item["date"])
    entry.description(item["duration"])
    entry.link(href=item['URL'])


# In[6]:


#feed.rss_str(pretty=True)
feed.rss_file(f"{USERNAME}_feed.rss")

