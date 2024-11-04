import requests
from bs4 import BeautifulSoup
from get_cards import get_monkeys


def get_html(url) -> str:
    response = requests.get(url)
    return response.text

URL = 'https://bloons.fandom.com/wiki/Bloons_Card_Storm'
html = get_html(URL)
soup = BeautifulSoup(html, 'html.parser')

monkeys = get_monkeys(soup)
for monkey in monkeys:
    print(monkey)



