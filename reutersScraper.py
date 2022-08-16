from pprint import pprint
import requests
from bs4 import BeautifulSoup


# Blueprint: Using an HTML Parser for Extraction:

url = 'https://www.reuters.com/article/us-health-vaping-marijuana-idUSKBN1WG4KT'

file = url.split("/")[-1] + ".html"

r = requests.get(url)

# Downloading the html page for further processing:
with open(file, "w+b") as f:
    f.write(r.text.encode('utf-8'))


with open(file, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Extracting the article title:
print(soup.h1.text)

# Extracting the article body
pprint(soup.select_one("div.ArticleBodyWrapper").text)

# Extracting the image caption
print(soup.select_one("div.WithCaption-caption-container-Y-li-").text)

# Extracting the url of the Article:
# The tag 'canonical' is not mandatory, but it is extremely common,
# as it is taken into account by search engines and contributes to a good ranking:
print(soup.find("link", {'rel': 'canonical'})['href'])

# Extracting the authors list:
sel = "div.ArticleBody-byline-container-3H6dy > p"
print(soup.select(sel))
print([a.text for a in soup.select(sel)])

# Extracting the category of the article:
print(soup.select_one("div.ArticleHeader-info-container-3-6YG").text)
