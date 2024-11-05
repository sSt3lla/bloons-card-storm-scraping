from bs4 import BeautifulSoup, Tag, NavigableString
from cards import Monkey, Rarity, Bloon, Power, Hero
from bs4.element import ResultSet
from re import match
from functools import cache
from typing import Optional, cast

_powers_initialized: list[Power] = []

@cache
def get_monkeys(soup: BeautifulSoup) -> list[Monkey]:
    return _extract_objects(soup, 1, _parse_monkey_data)

@cache
def get_bloons(soup: BeautifulSoup) -> list[Bloon]:
    return _extract_objects(soup, 2, _parse_bloon_data)

def get_powers(soup: BeautifulSoup) -> list[Power]:
    """Get powers, using the cached version if it exists and has been initialized with heroes."""
    global _powers_initialized
    if not _powers_initialized:
        _powers_initialized = _extract_objects(soup, 3, _parse_power_data)
    return _powers_initialized

@cache
def get_heros(soup: BeautifulSoup) -> list[Hero]:
    heros: list[Hero] = []
    all_powers = get_powers(soup)
    power_by_name = {p.name: p for p in all_powers}
    
    for tr in _get_tr_tags(soup, 0):
        tds = _replace_br_with_newline(tr.findAll('td'))
        name = _extract_text(tds[1])

        abilities: dict[int, str] = {}
        for a in tds[2].text.strip().split('\n'):
            parsed_bloon = _parse_bloon_string(a)
            for k, v in parsed_bloon.items():
                abilities[int(k)] = v
        
        unique_power_names = tds[3].text.strip().split('\n')
        unique_powers = [power_by_name[name] for name in unique_power_names if name in power_by_name]

        hero = Hero(name, abilities, unique_powers)
        
        # Update the hero reference in the power objects
        for power in unique_powers:
            power.hero = hero

        heros.append(hero)
    return heros

def _extract_objects(soup: BeautifulSoup, table_index: int, parse_fn):
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

    # We update the power card later to include the hero
    return Power(name, description, cost, rarity, hero=None)

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