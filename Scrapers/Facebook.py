# https://engineering.fb.com/2008/5
# fb_content_type-article

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from Utility import Article
from Utility import CompanyData
from Utility import Database


company_id = CompanyData.get_company_id("Facebook")


def get_articles():
    today = datetime.today()
    links = {"set"}

    for year in range(2008, today.year + 1):
        print("loading year:", year)
        for month in range(1, 13):
            cur_url = "https://engineering.fb.com/" + str(year) + "/" + str(month).zfill(2) + "/"
            html_text = requests.get(cur_url).text
            soup = BeautifulSoup(html_text, 'lxml')
            all_links = soup.find_all("a", href=True)

            for link in all_links:
                if link["href"][0:len(cur_url)] == cur_url:
                    links.add(link["href"])

    links.remove("set")

    return convert_links_to_articles(links)


def get_article(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    title = get_title(soup)
    date_posted = get_date(soup)

    return Article.Article(url, title, company_id, date_posted)


def get_title(soup):
    title_tag = soup.find(class_='entry-title')
    title = title_tag.text
    return title


def get_date(soup):
    time_tag = soup.find(class_='entry-date')
    datetime_tag = time_tag.next_element
    raw_time = datetime_tag.get_attribute_list("datetime")[0]
    return raw_time


def convert_links_to_articles(links):
    articles = []
    for link in links:
        print("loading article:", link)
        articles.append(get_article(link))

    return articles


Database.insert_articles(get_articles(), company_id)

