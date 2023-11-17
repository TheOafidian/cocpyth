from enum import Enum
from pydantic.dataclasses import dataclass
from cocpyth.dtypes.dice import d4, d6
from cocpyth.dtypes.skills import SKILLS1920
from cocpyth.dtypes.occupations import Occupation
from cocpyth.utils.weird_math import cthulhu_round
import cocpyth.dtypes.stats as stats


@dataclass
class Character:
    first_name: str
    last_name: str
    sanity: stats.Sanity = stats.Sanity()
    strength: stats.Strength = stats.Strength()
    dexterity: stats.Dexterity = stats.Dexterity()
    size: stats.Size = stats.Size()
    constitution: stats.Constitution = stats.Constitution()
    intelligence: stats.Intelligence = stats.Intelligence()
    education: stats.Education = stats.Education()
    power: stats.Power = stats.Power()
    appearance: stats.Appearance = stats.Appearance()
    luck: stats.Luck = stats.Luck()
    hp: stats.Hitpoints = stats.Hitpoints()
    mp: stats.Magicpoints = stats.Magicpoints()

    def __post_init__(self):
        self.full_name = self.first_name + " " + self.last_name
        self.sanity.current = self.power.current
        self.hp.current = cthulhu_round((self.constitution.current + self.size.current) / 10)
        self.mp.current = self.power.current / 5
        self.skills = SKILLS1920
        self.skills.dodge.set(self.dexterity.current/2)
        self.damage_bonus, self.build = self._determine_build_db()
        self.moverate = self._determine_move_rate()

    def _determine_build_db(self):
        physique = self.strength.current + self.size.current

        if physique < 65:
            return -2, -2
        elif physique < 85:
            return -1, -1
        elif physique < 125:
            return 0, 0
        elif physique < 165:
            return d4, 1
        else: return d6, 2

    def _determine_move_rate(self):

        STR = self.strength.current
        DEX = self.dexterity.current
        SIZ = self.size.current

        if STR < SIZ and DEX < SIZ:
            return 7
        if STR > SIZ and DEX > SIZ:
            return 9
        return 8
    
    def add_occupation(self, occupation: Occupation):
        print(occupation)
        raise NotImplementedError

class GenderEnum(str, Enum):
    M = "male"
    F = "female"


if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve.skills.jump)
    print(steve.skills.jump + 10)
    print(steve.skills.jump)
    # for skills with spaces
    print(steve.skills.arts_and_crafts)
