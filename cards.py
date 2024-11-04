from enum import unique, StrEnum, auto
from dataclasses import dataclass

@unique
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
class Card:
    """Base class for all cards."""
    name: str
    description: str
    cost: int
    rarity: Rarity
        
@dataclass
class Monkey(Card):
    """Class that represents a monkey card."""
    damage: int
    ammo: int
    reload: int

@dataclass
class Bloon(Card):
    """Class that represents a bloon"""
    charge: int
    damage: int
    delay: int

@dataclass
class Power(Card):
    """Class that represents a power card."""
    pass