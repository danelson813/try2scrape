# try2scrape/main.py

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import pandas as pd
from loguru import logger

results = []
for i in range(1, 11):
    url = f"https://quotes.toscrape.com/page/{i}/"
    logger.info(f"url: {url}")
    ua = UserAgent()
    headers = {"user-agent": ua.random}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, "html.parser")

    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        result = {
            "item": quote.find("span", class_="text").text,
            "author": quote.find("small", class_="author").text,
            "tags": [item.text for item in quote.find_all("a", class_="tag")],
        }
        print(result)
        results.append(result)
data = pd.DataFrame(results)
data.to_csv("data/results.csv", index=False)
