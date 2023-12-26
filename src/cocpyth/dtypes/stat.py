import logging
from pydantic import BaseModel, PositiveInt, NonNegativeInt
from cocpyth.dtypes.dice import d6
from cocpyth.utils.weird_math import cthulhu_round


class Stat(BaseModel):
    name: str
    game_over: str
    max: PositiveInt = 100
    min: NonNegativeInt = 0
    current: NonNegativeInt = 0
    half: NonNegativeInt = 10
    fifth: NonNegativeInt = 4
    
    def _set_half_and_fifth(self):
        self.half = cthulhu_round(self.current / 2)
        self.fifth = cthulhu_round(self.current / 5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_half_and_fifth()

    def get(self):
        if self.current <= 0:
            logging.error(self.game_over)
        return self.current

    def set(self, value):
        self.current = value

    def __repr__(self) -> str:
        return "{}: {}".format(self.name, self.current)

    def __str__(self) -> str:
        return "{}: {}".format(self.name, self.current)

    def __add__(self, x):
        temp = self.model_copy()
        temp.current += x
        return temp

    def __iadd__(self, x):
        self.current += x
        return self

    def __sub__(self, x):
        temp = self.model_copy()
        temp.current -= x
        return temp

    def __isub__(self, x):
        self.current -= x
        return self

    def __mul__(self, x):
        temp = self.model_copy()
        temp.current *= x
        return temp

    def __truediv__(self, x):
        temp = self.model_copy()
        temp.current = cthulhu_round(temp.current / x) 
        return temp

    def __idiv__(self, x):
        self.current = cthulhu_round(self.current / x)
        return self

    def __ge__(self, x):
        return self.current >= x

    def __gt__(self, x):
        return self.current > x

    def __le__(self, x):
        return self.current <= x

    def __lt__(self, x):
        return self.current < x

    def __pos__(self):
        return self.current

    def __neg__(self):
        return -self.current
    
    def __eq__(self, other):
        return self.current == other.current and self.name == other.name


strength_settings = {
    "name": "Strength",
    "current": 5 * d6.rolln(3),
    "game_over": "Your frail body succumbs under its own weight. You are unable to move.",
}


class Strength(Stat):
    def __init__(self):
        super(Strength, self).__init__(**strength_settings)


constitution_settings = {
    "name": "Constitution",
    "current": 5 * d6.rolln(3),
    "game_over": "Your sickness beats you in your final hour, you drop dead to the floor.",
}


class Constitution(Stat):
    def __init__(self):
        super(Constitution, self).__init__(**constitution_settings)


dexterity_settings = {
    "name": "Dexterity",
    "current": 5 * d6.rolln(3),
    "game_over": "You are unable to coordinate your body and can no longer perform physical tasks.",
}


class Dexterity(Stat):
    def __init__(self):
        super(Dexterity, self).__init__(**dexterity_settings)


appearance_settings = {
    "name": "Appearance",
    "current": 5 * d6.rolln(3),
    "game_over": "You are a horrid person both inside and out. People no longer talk to you, you spend the rest of your life alone.",
}


class Appearance(Stat):
    def __init__(self):
        super(Appearance, self).__init__(**appearance_settings)


intelligence_settings = {"name": "Size", "current": 5 * (d6.rolln(2) + 6), "game_over": "You've just dissapeared."}


class Size(Stat):
    def __init__(self):
        super(Size, self).__init__(**intelligence_settings)


size_settings = {"name": "Size", "min": 35, "current": 5 * (d6.rolln(2) + 6), "game_over": "You've just dissapeared."}


class Size(Stat):
    def __init__(self):
        super(Size, self).__init__(**size_settings)


intelligence_settings = {
    "name": "Intelligence",
    "current": 5 * (d6.rolln(2) + 6),
    "game_over": "You are in a state of drooling and babbling.",
}


class Intelligence(Stat):
    def __init__(self):
        super(Intelligence, self).__init__(**intelligence_settings)


education_settings = {"name": "Education", "current": 5 * (d6.rolln(2) + 6), "game_over": "You lose your memory."}


class Education(Stat):
    def __init__(self):
        super(Education, self).__init__(**education_settings)


luck_settings = {"name": "Luck", "current": 5 * (d6.rolln(3)), "game_over": "Misfortune befalls you."}


class Luck(Stat):
    def __init__(self):
        super(Luck, self).__init__(**luck_settings)


power_settings = {
    "name": "Power",
    "current": 5 * (d6.rolln(3)),
    "game_over": "You wander the streets in a zombie-like fashion.",
}


class Power(Stat):
    def __init__(self):
        super(Power, self).__init__(**power_settings)


sanity_settings = {"name": "Sanity", "current": 5 * (d6.rolln(2) + 6), "game_over": "You are driven insane!"}


class Sanity(Stat):
    def __init__(self):
        super(Sanity, self).__init__(**sanity_settings)


hitpoints_settings = {
    "name": "Hitpoints",
    "current": 10,
    "max": 20,
    "game_over": "You bleed out from your wounds and die.",
}


class Hitpoints(Stat):
    def __init__(self):
        super(Hitpoints, self).__init__(**hitpoints_settings)


magicpoints_settings = {
    "name": "Magicpoints",
    "current": 10,
    "max": 20,
    "game_over": "NA"
}

class Magicpoints(Stat):
    def __init__(self):
        super(Magicpoints, self).__init__(**magicpoints_settings)

