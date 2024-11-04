import requests
from bs4 import BeautifulSoup
from get_cards import get_bloons, get_monkeys, get_powers, get_heros


def get_html(url) -> str:
    response = requests.get(url)
    return response.text

URL = 'https://bloons.fandom.com/wiki/Bloons_Card_Storm'
html = get_html(URL)
soup = BeautifulSoup(html, 'html.parser')

monkeys = get_monkeys(soup)
for monkey in monkeys:
    print(monkey)
    # print()

# print()
# print()

bloons = get_bloons(soup)
for bloon in bloons:
    print(bloon)
#     print()

# print()
# print()

powers = get_powers(soup)
for power in powers:
    print(power)
    # print()

heros = get_heros(soup)
for hero in heros:
    print(hero)
    # print()