from math import sqrt

def state_power(talent_stars: float, knight_level: float, book_bonus: float) -> float:
    """
    Calculate Knight State Power.
    Formula: (talent_stars * knight_level * 20) + (100 * sqrt(book_bonus))
    """
    return (talent_stars * knight_level * 20) + (100 * sqrt(book_bonus))

def talent_bonus(talent_stars: float, level: int) -> float:
    """
    Calculate Knight Talent Bonus.
    Formula: (talent_stars / 10) * (100 + 3 * (level - 1) + (level - 1)^2)
    """
    return (talent_stars / 10) * (100 + 3 * (level - 1) + (level - 1) ** 2)

def lover_ballroom(charm: float) -> float:
    """
    Calculate Lover Power from Ballroom.
    Formula: 67 * charm * ((charm + 100) / 1000)
    """
    return 67 * charm * ((charm + 100) / 1000)

def lover_greeting(charm: float) -> float:
    """
    Calculate Lover Power from Greeting.
    Formula: 3 * charm * ((charm + 100) / 1000)
    """
    return 3 * charm * ((charm + 100) / 1000)
