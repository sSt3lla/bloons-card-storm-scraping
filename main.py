import requests
from bs4 import BeautifulSoup
import json

from scrapper import get_bloons, get_heros, get_monkeys, get_powers, CardEncoder

URL = 'https://bloons.fandom.com/wiki/Bloons_Card_Storm'
html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

monkeys = get_monkeys(soup)
bloons = get_bloons(soup)
heros = get_heros(soup)
powers = get_powers(soup)

cards = monkeys + bloons + heros + powers
json_cards = json.dumps(cards, cls=CardEncoder, indent=4)
print(json_cards)