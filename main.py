import requests
from bs4 import BeautifulSoup

from scrapper import get_bloons, get_heros, get_monkeys, get_powers

URL = 'https://bloons.fandom.com/wiki/Bloons_Card_Storm'
html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

monkeys = get_monkeys(soup)
bloons = get_bloons(soup)
heros = get_heros(soup)
powers = get_powers(soup)

for monkey in monkeys:
    print(monkey)

for bloon in bloons:
    print(bloon)

for power in powers:
    print(power)

for hero in heros:
    print(hero)