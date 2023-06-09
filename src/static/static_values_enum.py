from enum import Enum

league_ratings_all = [0, 400, 700, 1000, 1300, 1600, 1900, 2200, 2500, 2800, 3100, 3400, 3700, 4200, 4700, 5100]
league_ratings = [0, 100, 1000, 1900, 2800, 3700]
league_colors = ['lightgray', 'brown', 'gray', 'yellow', 'purple', 'orange']


class Format(Enum):
    MODERN = 'modern'
    WILD = 'wild'


class MatchType(Enum):
    CHALLENGE = 'Challenge'
    RANKED = 'Ranked'
    TOURNAMENT = 'Tournament'


class CardType(Enum):
    summoner = 'Summoner'
    monster = 'Monster'


class Leagues(Enum):
    NOVICE = 0
    BRONZE_III = 1
    BRONZE_II = 2
    BRONZE_I = 3
    SILVER_III = 4
    SILVER_II = 5
    SILVER_I = 6
    GOLD_III = 7
    GOLD_II = 8
    GOLD_I = 9
    DIAMOND_III = 10
    DIAMOND_II = 11
    DIAMOND_I = 12
    CHAMPION_III = 13
    CHAMPION_II = 14
    CHAMPION_I = 15


class RatingLevel(Enum):
  Novice = 0
  Bronze = 1
  Silver =2
  Gold = 3
  Diamond = 4
  Champion = 5


class Edition(Enum):
    alpha = 0
    beta = 1
    promo = 2
    reward = 3
    untamed = 4
    dice = 5
    gladius = 6
    chaos = 7
    rift = 8
    soulbound = 10


class Element(Enum):
    water = 'Blue'
    death = 'Black'
    fire = 'Red'
    life = 'White'
    dragon = 'Gold'
    earth = 'Green'
    neutral = 'Gray'


class Rarity(Enum):
    common = 1
    rare = 2
    epic = 3
    legendary = 4


class ManaCap(Enum):
    low = '0-20'
    medium = '21-40'
    high = '41-60'
    max = '61-999'


def get_list_of_enum(enum):
    return list(map(lambda x: x.value, enum._member_map_.values()))
