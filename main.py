import requests
from bs4 import BeautifulSoup

from get_cards import get_bloons, get_heros, get_monkeys, get_powers

URL = 'https://bloons.fandom.com/wiki/Bloons_Card_Storm'
html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

monkeys = get_monkeys(soup)
bloons = get_bloons(soup)
get_powers(soup)
heros = get_heros(soup)   # Heroes update the power references
powers = get_powers(soup)  # Get the same powers with hero references

# Print everything
for power in powers:
    print(power)  # Now shows hero references