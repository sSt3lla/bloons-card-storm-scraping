from bs4 import BeautifulSoup, Tag
from cards import Monkey, Rarity, Bloon, Power
from bs4.element import ResultSet

def get_monkeys(soup: BeautifulSoup) -> list[Monkey]:
    '''This function will return a list of Monkey objects'''
    monkeys: list[Monkey] = []
    
    #<table class="wikitable sortable jquery-tablesorter" data-index-number="3">
    #I could not find the table with the monkeys so I'm doing this instead
    monkey_table: Tag = soup.findAll("table", {"class": "wikitable"})[1]    
    tbody: Tag = monkey_table.find("tbody")
    all_tr: ResultSet[Tag] = tbody.findAll("tr")

    monkey_tr = all_tr[1:]
    for tr in monkey_tr:
        # name = tr.find("td").text
        # print(name)
        all_td = tr.findAll("td")

        # Replace all <br> with a newline
        for tag in all_td:
            all_br = tag.findAll("br")
            for br in all_br:
                br.replace_with('\n')

        image_td = all_td[0]

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
            damage = 0
        else:
            damage = int(damage)
        
        ammo_td = all_td[5]
        ammo = _extract_playable(ammo_td)
        if ammo == 'N/A':
            ammo = 0
        else:
            ammo = int(ammo)

        reload = all_td[6]
        reload = _extract_playable(reload)
        if reload == 'N/A':
            reload = 0
        else:
            reload = int(reload)
        rarity_td = all_td[7]

        text = rarity_td.text.strip().replace(' ', '_')

        # This is a bad fix, but I don't know why its happening
        if text == '':
            text = 'COMMON'

        rarity = Rarity.from_string(text)
        monkey = Monkey(name, description, cost, rarity, damage, ammo, reload)
        monkeys.append(monkey)

    return monkeys

def get_bloons(soup: BeautifulSoup) -> list[Bloon]:
    '''This function will return a list of bloon objects'''
    bloons: list[Bloon] = []

    bloon_table: Tag = soup.findAll("table", {"class": "wikitable"})[2]

    tbody: Tag = bloon_table.find("tbody")
    all_tr: ResultSet[Tag] = tbody.findAll("tr")

    bloon_tr = all_tr[1:]

    for tr in bloon_tr:
        all_td = tr.findAll("td")

         # Replace all <br> with a newline
        for tag in all_td:
            all_br = tag.findAll("br")
            for br in all_br:
                br.replace_with('\n')

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

        bloon = Bloon(name, description, cost, charges, damage, delay, rarity)
        bloons.append(bloon)
    return bloons

def get_powers(soup: BeautifulSoup) -> list[Power]:
    '''This function will return a list of Power objects'''
    powers: list[Power] = []

    power_table: Tag = soup.findAll("table", {"class": "wikitable"})[3]

    tbody: Tag = power_table.find("tbody")
    all_tr: ResultSet[Tag] = tbody.findAll("tr")

    power_tr = all_tr[1:]

    for tr in power_tr:
        all_td = tr.findAll("td")

        # Replace all <br> with a newline
        for tag in all_td:
            all_br = tag.findAll("br")
            for br in all_br:
                br.replace_with('\n')

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

        power = Power(name, description, cost, rarity)
        powers.append(power)
    return powers

def _extract_playable(tag: Tag) -> str:
    '''This function will extract the text from a tag and remove any playable text'''
    text = tag.text
    
    split_text = ['(Full Playable - update)', '(Full Playable)','(First Release)']

    for split in split_text:
        if split in text:
            text = text.split(split)[0]
            break
    return text.strip()