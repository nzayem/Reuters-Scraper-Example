import requests
from bs4 import BeautifulSoup
import os.path
import glob
import pandas as pd


def download_archive_page(page):
    filename = 'page-%06d.html' % page

    if not os.path.isfile(filename):
        url = "https://www.reuters.com/news/archive/" + "?view=page&page=%d&pageSize=10" % page

        r = requests.get(url)
        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(r.text)


def parse_archive_page(page_file):
    with open(page_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    hrefs = ["https://www.reuters.com" + a['href'] for a in soup.select("article.story div.story-content a")]

    return hrefs


def download_article(url):
    # check if the article is already there
    filename = url.split('/')[-2] + '-article.html'
    if not os.path.isfile(filename):
        r = requests.get(url)
        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(r.text)


def find_obfuscated_class(soup, klass):
    return soup.find_all(lambda tag: tag.has_attr("class") and (klass in " ".join(tag["class"])))


def parse_article(article_file):

    with open(article_file, "r", encoding='utf-8') as f:
        html = f.read()
    r = {}
    soup = BeautifulSoup(html, 'html.parser')
    r['url'] = soup.find("link", {'rel': 'canonical'})['href']
    r['id'] = r['url'].split("-")[-1]
    r['headline'] = soup.h1.text
    r['text'] = "\n".join([t.text for t in find_obfuscated_class(soup, "Paragraph-paragraph")])
    r['time'] = soup.find("meta", {'property': "og:article:published_time"})['content']

    return r


# Download 10 pages of the archive:
for i in range(1, 10):
    download_archive_page(i)

print('Downloading pages complete')

# parse archive and add to article_urls
article_urls = []
for page_file in glob.glob('page-*.html'):
    article_urls += parse_archive_page(page_file)

for url in article_urls:
    print(url)

print('Parsing Complete')

# Download articles:
for url in article_urls:
    download_article(url)

print('Downloading articles complete')

# Create and arrange in a pandas dataframe:
df = pd.DataFrame()
for article_file in glob.glob("*-article.html"):
    df = df.append(parse_article(article_file), ignore_index=True)

print(df.head())
