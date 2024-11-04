from bs4 import BeautifulSoup, Tag, NavigableString
from cards import Monkey, Rarity, Bloon, Power, Hero
from bs4.element import ResultSet
import re
from functools import cache

@cache
def get_monkeys(soup: BeautifulSoup) -> list[Monkey]:
    '''This function will return a list of Monkey objects'''
    monkeys: list[Monkey] = []

    for tr in _get_tr_tags(soup, 1):
        all_td: ResultSet[Tag] = tr.findAll('td')

        _replace_br_with_newline(all_td)

        name_td = all_td[1]
        name = name_td.text.strip()

        description_td = all_td[2]
        description = _extract_playable(description_td)
        if description == 'N/A':
            description = ''
        
        cost_td = all_td[3]
        cost = _extract_playable(cost_td)
        cost = int(cost)

        damage_td = all_td[4]
        damage = _extract_playable(damage_td)
        if damage == 'N/A':
            damage = None
        else:
            damage = int(damage)
        
        ammo_td = all_td[5]
        ammo = _extract_playable(ammo_td)
        if ammo == 'N/A':
            ammo = None
        else:
            ammo = int(ammo)

        reload = all_td[6]
        reload = _extract_playable(reload)
        if reload == 'N/A':
            reload = None
        else:
            reload = int(reload)
        rarity_td = all_td[7]

        text = rarity_td.text.strip().replace(' ', '_')

        rarity = Rarity.from_string(text)
        monkey = Monkey(name, description, cost, rarity, damage, ammo, reload)
        monkeys.append(monkey)

    return monkeys

@cache
def get_bloons(soup: BeautifulSoup) -> list[Bloon]:
    '''This function will return a list of bloon objects'''
    bloons: list[Bloon] = []

    for tr in _get_tr_tags(soup, 2):
        all_td: ResultSet[Tag] = tr.findAll('td')

        _replace_br_with_newline(all_td)

        name_td = all_td[1]
        name = name_td.text.strip()

        description_td = all_td[2]
        description = _extract_playable(description_td)
        if description == 'N/A':
            description = ''

        cost_td = all_td[3]
        cost = _extract_playable(cost_td)
        cost = int(cost)

        charges_td = all_td[4]
        charges = _extract_playable(charges_td)
        charges = int(charges)
        
        damage_td = all_td[5]
        damage = _extract_playable(damage_td)
        damage = int(damage)

        delay_td = all_td[6]
        delay = _extract_playable(delay_td)
        delay = int(delay)

        rarity_td = all_td[7]
        text = rarity_td.text.strip().replace(' ', '_')
        rarity = Rarity.from_string(text)

        is_large_criteria = ['MOAB', 'BFB', 'ZOMG']
        is_large = any(criteria in name for criteria in is_large_criteria)

        bloon = Bloon(name=name, 
                      description=description, 
                      cost=cost, 
                      rarity=rarity, 
                      charge=charges, 
                      damage=damage, 
                      delay=delay, 
                      is_large=is_large)
        bloons.append(bloon)
    return bloons

@cache
def get_powers(soup: BeautifulSoup) -> list[Power]:
    '''This function will return a list of Power objects'''
    powers: list[Power] = []

    for tr in _get_tr_tags(soup, 3):
        all_td: ResultSet[Tag] = tr.findAll('td')
        _replace_br_with_newline(all_td)

        name_td = all_td[1]
        name = name_td.text.strip()

        description_td = all_td[2]
        description = _extract_playable(description_td)
        if description == 'N/A':
            description = ''

        cost_td = all_td[3]
        cost = _extract_playable(cost_td)
        cost = int(cost)

        rarity_td = all_td[4]
        text = rarity_td.text.strip().replace(' ', '_')
        rarity = Rarity.from_string(text)

        power = Power(name, description, cost, rarity, hero=None)
        powers.append(power)
    return powers

@cache
def get_heros(soup: BeautifulSoup) -> list[Hero]:
    '''This function will return a list of Hero objects'''
    heros: list[Hero] = []

    for tr in _get_tr_tags(soup, 0):
        all_td: ResultSet[Tag] = tr.findAll("td")
        _replace_br_with_newline(all_td)

        name_td = all_td[1]
        name = name_td.text.strip()

        abilities_td = all_td[2]
        abilities = abilities_td.text.strip()
        abilities = abilities.split('\n')
        abilities = [_parse_bloon_string(ability) for ability in abilities]
        abilities = {key: value for ability in abilities for key, value in ability.items()}

        all_powers = get_powers(soup)

        unique_powers_td = all_td[3]
        unique_powers = unique_powers_td.text.strip()
        unique_powers = unique_powers.split('\n')

        unique_powers_list = [p for p in all_powers if p.name in unique_powers]

        hero = Hero(name, abilities, unique_powers_list)
        heros.append(hero)

    return heros

def _replace_br_with_newline(tag_list: ResultSet[Tag]) -> None:
    for tag in tag_list:
        [br.replace_with('\n') for br in tag.find_all("br")]


def _get_tr_tags(soup: BeautifulSoup, index: int) -> list[Tag]:
    '''This function will return all tr tags from a table'''

    #<table class="wikitable sortable jquery-tablesorter" data-index-number="3">
    table: Tag = soup.findAll('table', {'class': 'wikitable'})[index]

    tbody = _check_tag(table.find('tbody'))
    tr_tags: ResultSet[Tag] = tbody.findAll('tr')
    return tr_tags[1:]


def _parse_bloon_string(s: str) -> dict:
    '''Use regex to match the format "(x): text"'''
    match = re.match(r"\((\d+)\):\s*(.+)", s)
    assert match, f"Invalid bloon string: {s}"
    return {
        int(match.group(1)) : match.group(2)
    }


def _extract_playable(tag: Tag) -> str:
    '''This function will extract the text from a tag and remove any playable text'''
    text = tag.text
    
    split_text = ['(Full Playable - update)', '(Full Playable)','(First Release)']

    for split in split_text:
        if split in text:
            text = text.split(split)[0]
            break
    return text.strip()

def _check_tag(tag: Tag | NavigableString | None) -> Tag:
    '''This function will check if a tag is empty and return N/A if it is'''
    assert isinstance(tag, Tag), 'Tag is not a Tag'
    return tag