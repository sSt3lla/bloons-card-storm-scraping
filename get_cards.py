from functools import cache
from re import match
from typing import Optional, cast

from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.element import ResultSet

from cards import Bloon, Hero, Monkey, Power, Rarity


@cache
def get_monkeys(soup: BeautifulSoup) -> list[Monkey]:
    return _extract_objects(soup, 1, _parse_monkey_data)

@cache
def get_bloons(soup: BeautifulSoup) -> list[Bloon]:
    return _extract_objects(soup, 2, _parse_bloon_data)

@cache
def get_powers(soup: BeautifulSoup) -> list[Power]:
    return _get_heros_and_powers(soup)[1]

@cache
def get_heros(soup: BeautifulSoup) -> list[Hero]:
    return _get_heros_and_powers(soup)[0]
    
@cache
def _get_heros_and_powers(soup: BeautifulSoup) -> tuple[list[Hero], list[Power]]:
    heros: list[Hero] = []
    
    for tr in _get_tr_tags(soup, 0):
        tds = _replace_br_with_newline(tr.findAll('td'))
        name = _extract_text(tds[1])

        abilities: dict[int, str] = {}
        for a in _extract_text(tds[2]).split('\n'):
            parsed_bloon = _parse_bloon_string(a)
            for k, v in parsed_bloon.items():
                abilities[int(k)] = v
        
        powers: list[str] = _extract_text(tds[3]).split('\n')

        hero = Hero(name, abilities, powers)
        heros.append(hero)
    
    power_cards: list[Power] = _extract_objects(soup, 3, _parse_power_data)

    # Now we update all references
    for power in power_cards:
        for hero in heros:
            if power.name in hero.unique_powers:
                power.hero = hero
                hero.unique_powers.remove(power.name)
                hero.unique_powers.append(power)
                break
            
    return heros, power_cards  


def _extract_objects(soup: BeautifulSoup, table_index: int, parse_fn) -> list[object]:
    objects = []
    for tr in _get_tr_tags(soup, table_index):
        tds = _replace_br_with_newline(tr.findAll('td'))
        str_tds = [_extract_text(td) for td in tds]
        objects.append(parse_fn(str_tds))
    return objects

def _parse_monkey_data(tds: list[str]) -> Monkey:
    name = tds[1]
    description = _extract_playable(tds[2])
    cost = int(_extract_playable(tds[3]))
    damage = optional_int(_extract_playable(tds[4]))
    ammo = optional_int(_extract_playable(tds[5]))
    reload_time = optional_int(_extract_playable(tds[6]))
    rarity = Rarity.from_string(tds[7].replace(' ', '_'))
    return Monkey(name, description, cost, rarity, damage, ammo, reload_time)

def _parse_bloon_data(tds: list[str]) -> Bloon:
    name = tds[1]
    description = tds[2]
    cost = int(tds[3])
    charges = int(tds[4])
    damage = int(tds[5])
    delay = int(tds[6])
    rarity = Rarity.from_string(tds[7].replace(' ', '_'))
    is_large = any(x in name.upper() for x in ['MOAB', 'BFB', 'ZOMG'])

    return Bloon(name, description, cost, rarity, charges, damage, delay, is_large)

def _parse_power_data(tds: list[str]) -> Power:
    name = tds[1]
    description = tds[2]
    cost = int(tds[3])
    rarity = Rarity.from_string(tds[4].replace(' ', '_'))

    return Power(name, description, cost, rarity)

def _replace_br_with_newline(tag_list: ResultSet[Tag]) -> list[Tag]:
    for tag in tag_list:
        for br in tag.find_all("br"):
            br = cast(Tag, br)
            br.replace_with('\n')
    return tag_list

def _get_tr_tags(soup: BeautifulSoup, index: int) -> list[Tag]:
    table: Tag = soup.find_all('table', {'class': 'wikitable'})[index]
    tbody = _check_tag(table.find('tbody'))
    return tbody.find_all('tr')[1:]

def _parse_bloon_string(s: str) -> dict[int, str]:
    matched = match(r"\((\d+)\):\s*(.+)", s)
    assert matched, f"Invalid bloon string: {s}"
    return {int(matched.group(1)): matched.group(2)}

def _extract_playable(s: str) -> str:
    '''Extracts the playable text from a tag.'''
    for split_text in ['(Full Playable - update)', '(Full Playable)', '(First Release)']:
        if split_text in s:
            return s.split(split_text)[0].strip()
    return s

def _check_tag(tag: Tag | NavigableString | None) -> Tag:
    assert isinstance(tag, Tag), 'Tag is not a valid HTML Tag'
    return tag

def _extract_text(tag: Tag) -> str:
    return tag.text.strip()

def optional_int(value: str) -> Optional[int]:
    '''Converts a string to an integer if possible, otherwise returns None.'''
    try:
        return int(value) if value != 'N/A' else None
    except ValueError:
        return None