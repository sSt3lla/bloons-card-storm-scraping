from json import JSONEncoder

from .cards import Bloon, Hero, Monkey, Power


class CardEncoder(JSONEncoder):
    def default(self, obj):
        match obj:
            case Monkey():
                return self._monkey_to_dict(obj)
            case Bloon():
                return self._bloon_to_dict(obj)
            case Hero():
                return self._hero_to_dict(obj)
            case Power():
                return self._power_to_dict(obj)
            case _:
                return super().default(obj)

    def _monkey_to_dict(self, monkey: Monkey) -> dict:
        return {
            'type': 'monkey',
            'data':     
            {
                'name': monkey.name,
                'description': monkey.description,
                'cost': monkey.cost,
                'rarity': monkey.rarity,
                'damage': monkey.damage,
                'ammo': monkey.ammo,
                'reload': monkey.reload
            }
        }

    def _bloon_to_dict(self, bloon: Bloon) -> dict:
        return {
            'type': 'bloon',
            'data':     
            {
                'name': bloon.name,
                'description': bloon.description,
                'cost': bloon.cost,
                'rarity': bloon.rarity,
                'charge': bloon.charge,
                'damage': bloon.damage,
                'delay': bloon.delay,
                'is_large': bloon.is_large
            }
        }

    def _hero_to_dict(self, hero: Hero) -> dict:
        return {
            'type': 'hero',
            'data':     
            {
                'name': hero.name,
                'abilities': hero.abilities,
                'unique_powers': [p for p in hero.unique_powers]
            }
        }
    
    def _power_to_dict(self, power: Power) -> dict:
        return {
            'type': 'power',
            'data':     
            {
                'name': power.name,
                'description': power.description,
                'hero': power.hero.name if power.hero else ''
            }
        }