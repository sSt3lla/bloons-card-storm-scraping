from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional


class Rarity(StrEnum):
    """Enum class that represents the rarity of a card."""
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    SUPER_RARE = auto()
    ULTRA_RARE = auto()

    @classmethod
    def from_string(cls, name: str):
        """Custom constructor that returns an enum instance based on a string."""
        try:
            return cls[name.upper()]  # Convert to uppercase to match enum names
        except KeyError:
            raise ValueError(f"{name} is not a valid Rarity")

@dataclass
class Hero:
    """Class that represents a hero."""
    name: str
    abilities: dict[int, str]

    #Todo add comment explaing this
    unique_powers: list['Power']


@dataclass
class Card:
    """Base class for all cards."""
    name: str
    description: str
    cost: int
    rarity: Rarity
        
@dataclass
class Monkey(Card):
    """Class that represents a monkey card."""
    damage: Optional[int]
    ammo: Optional[int]
    reload: Optional[int]

@dataclass
class Bloon(Card):
    """Class that represents a bloon"""
    charge: int
    damage: int
    delay: int
    is_large: bool

@dataclass
class Power(Card):
    """Class that represents a power card."""
    hero: Optional[Hero] = None