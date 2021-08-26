from bs4 import BeautifulSoup
import requests
from datetime import datetime
from Utility import Article


def get_riot_article(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    title = get_riot_title(soup)
    date_posted = get_riot_date(soup)
    return Article.Article(url, title, "Riot", date_posted)


def get_riot_title(soup):
    title_tag = soup.find(class_='c-excerpt__title')
    raw_title = title_tag.text
    title = raw_title.replace("\n", "")
    return title


def get_riot_date(soup):
    time_tag = soup.find(class_='c-header__date')
    raw_time = time_tag.get_attribute_list("datetime")[0]
    year_to_minute = raw_time[0:len(raw_time) - 3]
    return datetime.strptime(year_to_minute, "%Y-%m-%dT%H:%M")


def get_riot_articles():
    url_paginated = "https://technology.riotgames.com/node?page="
    links = {}

    # when I created this I went through all 10 pages. I should only need to check the most recent now
    for i in range(1):
        print("Loaded page:", i)
        html_text = requests.get(url_paginated + str(i)).text
        soup = BeautifulSoup(html_text, 'lxml')
        all_links = soup.find_all("a", href=True)

        for link in all_links:
            href = link['href']
            valid_start = "/news"
            index = href.find(valid_start)

            if index != -1:
                if href.find("na.leagueoflegends.com") != -1:
                    continue
                if href == "https://technology.riotgames.com/news/feed":
                    continue
                if href == "http://www.riotgames.com/news":
                    continue
                if href[0:4] == "http":
                    full_url = href
                else:
                    full_url = "https://technology.riotgames.com" + href
                links[full_url] = {}

    riot_articles = []
    for valid_url in links:
        riot_articles.append(get_riot_article(valid_url))

    return riot_articles
