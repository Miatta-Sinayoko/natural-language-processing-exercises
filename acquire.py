import requests
from bs4 import BeautifulSoup
import os
import json


# # Acquire
# from env import host, user, password

# # Create a function that retrieves the necessary connection URL.

# def get_connection(db_name):
#     '''
#     This function uses my info from my env file to
#     create a connection url to access the Codeup db.
#     '''
#     return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

# Set user agent for requests
headers = {'User-Agent': 'Codeup Data Science'}

def get_soup(url):
    """
    Get BeautifulSoup object from a URL.
    """
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

# Define function to scrape blog articles

def scrape_blog_article(article_url):
    """
    Scrape information from a single blog article.
    """
    soup = get_soup(article_url)
    title = soup.find("h1").text
    date_published = soup.find('span', class_="published").text
    content = soup.find('div', class_="entry-content").text
    return {
        "title": title,
        "link": article_url,
        "date_published": date_published,
        "content": content
    }

# Define function to scrape news summaries from one page

def scrape_news_summary(topic):
    """
    Scrape news summaries based on a topic.
    """
    base_url = "https://inshorts.com/en/read/"
    soup = get_soup(base_url + topic)
    titles = soup.find_all('span', itemprop="headline")
    summaries = soup.find_all('div', itemprop="articleBody")
    
    return [{
        "category": topic,
        "title": titles[i].text,
        "content": summaries[i].text
    } for i in range(len(titles))]

def get_blog_articles(article_list):
    """
    Scrape and return blog articles' information from a list of URLs.
    """
    file = "blog_posts.json"
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    
    article_info = [scrape_blog_article(article) for article in article_list]

    with open(file, "w") as f:
        json.dump(article_info, f)
    
    return article_info
# Define function to scrape news articles based on a list of topics

def get_news_articles(topic_list):
    """
    Scrape and return news summaries based on a list of topics.
    """
    
     # Check if JSON file exists, load if it exist
    file = "news_articles.json"
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    
    final_list = [summary for topic in topic_list for summary in scrape_news_summary(topic)]

    # Save scraped data in JSON file
    with open(file, "w") as f:
        json.dump(final_list, f)
    
    return final_list
