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


# In[3]:


page_raw = req.get(URL)

if page_raw.status_code != 200:
    print(f"Invalid page: Status {page_raw.status_code}")
    exit


# In[4]:


page_soup = bs(page_raw.content, 'html.parser')
page_articles = page_soup.find_all("article")


# In[5]:


data_dict = []

for n, article in enumerate(page_articles):
    data_dict.append({
        'title': article.h3.text,
        'date': article.time["datetime"],
        'duration': article.span["data-value"],
        'URL': article.a["href"]
    })


# In[6]:


feed = FeedGenerator()
feed.id(URL)
feed.title(USERNAME)
feed.link(rel="self", href=URL)
feed.description(USERNAME) # Requires a description but none given on Rumble

for item in data_dict:
    entry = feed.add_entry()
    entry.id(item['URL'])
    entry.title(item["title"])
    entry.pubDate(item["date"])
    entry.description(item["duration"])
    entry.link(href=item['URL'])


# In[7]:


#feed.rss_str(pretty=True)
feed.rss_file(f"{USERNAME}_feed.rss")

